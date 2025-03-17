import os
import argparse
import asyncio
import re
import string
from concurrent.futures import ThreadPoolExecutor
import sys
import shlex

from examples.multiAgentQuestionGenerator.roles.CreatChooseRole import Teacher
from examples.multiAgentQuestionGenerator.roles.CreatFillRole import Teacher1
from examples.multiAgentQuestionGenerator.roles.CreatJudgeRole import Teacher2
from examples.multiAgentQuestionGenerator.roles.CreatSummaryRole import CreateSummaryRole
from examples.multiAgentQuestionGenerator.roles.GetPdf import GetPdf
from examples.multiAgentQuestionGenerator.roles.ReadPdf import ReadPdf
from examples.multiAgentQuestionGenerator.roles.SummaryReviewer import SummaryReviewer
from examples.multiAgentQuestionGenerator.roles.TestReviewer import Reviewer

import pdfplumber
from metagpt.team import Team
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, Text, String, Numeric
from sqlalchemy.orm import Session

import shutil
import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# 指定要监控的文件夹和目标文件夹
watch_folder = 'input'
dest_folder = 'output'

# 确保目标文件夹存在
if not os.path.exists(dest_folder):
    os.makedirs(dest_folder)

sys.stdout.reconfigure(encoding='utf-8')

print("开始运行")
# 设置数据库连接
DATABASE_URL = "mysql+pymysql://root:root@localhost/test_paper_generation"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 定义题目的数据库模型
class Question(Base):
    __tablename__ = "questionbank"
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(Text, nullable=False)
    answer = Column(String(255), nullable=False)
    topic_type = Column(String(255), nullable=False)
    score = Column(Numeric(10, 1), nullable=False)
    difficulty = Column(Integer, nullable=False)
    chapter_1 = Column(String(255), nullable=False)
    chapter_2 = Column(String(255), nullable=False)
    label_2 = Column(String(255), nullable=False)

def add_question_to_db(db: Session, questions_text: string):
    session = SessionLocal()
    try:
        questions = questions_text.split('++++++')
        for question_text in questions:
            if not question_text.strip():
                continue

            parts = question_text.split('\n')
            topic = answer = topic_type = score = difficulty = chapter_1 = chapter_2 = label_2 = None

            for part in parts:
                if '题目：' in part:
                    topic = part.replace('题目：', '').strip()
                elif '答案：' in part:
                    answer = part.replace('答案：', '').strip()
                elif '答案解释：' in part:
                    label_2 = part.replace('答案解释：', '').strip()
                elif '题目类型：' in part:
                    topic_type = part.replace('题目类型：', '').strip()
                elif '分数：' in part:
                    score = float(part.replace('分数：', '').strip())
                elif '难度：' in part:
                    difficulty = int(part.replace('难度：', '').strip())
                elif '主章节来源：' in part:
                    chapter_1 = part.replace('主章节来源：', '').strip()
                elif '次章节来源：' in part:
                    chapter_2 = part.replace('次章节来源：', '').strip()

            if all([topic, answer, topic_type, score is not None, difficulty is not None]):
                new_question = Question(
                    topic=topic, answer=answer, topic_type=topic_type, score=score,
                    difficulty=difficulty, chapter_1=chapter_1, chapter_2=chapter_2, label_2=label_2)
                session.add(new_question)

        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()

executor = ThreadPoolExecutor(max_workers=1)

async def read_pdf_all_pages(pdf_path):
    loop = asyncio.get_event_loop()
    text = await loop.run_in_executor(executor, lambda: _read_pdf_all_pages(pdf_path))
    return text

def _read_pdf_all_pages(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

async def process_pdf_and_simulate(pdf_text: string, investment: float = 100.0, n_round: int = 2):
    team = Team()
    team.hire([ReadPdf(), CreateSummaryRole(), SummaryReviewer()])
    team.invest(investment=investment)
    team.run_project(pdf_text)
    result = await team.run(n_round=n_round)

    pattern = re.compile(r'(?<=CreateSummaryRole:).*?(?=SummaryReviewer:|$)', re.DOTALL)
    matches = pattern.finditer(result)
    last_match = next(matches, None)
    for match in matches:
        last_match = match

    return last_match.group().strip() if last_match else ""

async def choice(investment: float = 100.0, n_round: int = 2, summary: str = "", difficulty: str = "", num: str = "", label_1: str = "", label_2: str = ""):
    init = f"summary:{summary}\n\ndifficulty:{difficulty}\n\nnum:{num}\n\nlabel_1:{label_1}\n\nlabel_2:{label_2}"
    team = Team()
    team.hire([GetPdf(), Teacher(), Reviewer()])
    team.invest(investment=investment)
    team.run_project(init)
    result = await team.run(n_round=n_round)  # 异步调用
    pattern = re.compile(r'(?<=Teacher:).*?(?=Reviewer:|$)', re.DOTALL)
    matches = pattern.finditer(result)
    last_match = next(matches, None)
    for match in matches:
        last_match = match

    if last_match:
        add_question_to_db(db=SessionLocal(), questions_text=last_match.group().strip())
    return last_match.group().strip() if last_match else "No CreateQuestion content found."
async def judgement(investment: float = 100.0, n_round: int = 2, summary: str = "", difficulty: str = "", num: str = "", label_1: str = "", label_2: str = ""):
    init = f"summary:{summary}\n\ndifficulty:{difficulty}\n\nnum:{num}\n\nlabel_1:{label_1}\n\nlabel_2:{label_2}"
    team = Team()
    team.hire([GetPdf(), Teacher2(), Reviewer()])
    team.invest(investment=investment)
    team.run_project(init)
    result = await team.run(n_round=n_round)

    pattern = re.compile(r'(?<=Teacher2:).*?(?=Reviewer:|$)', re.DOTALL)
    matches = pattern.finditer(result)
    last_match = next(matches, None)
    for match in matches:
        last_match = match

    if last_match:
        add_question_to_db(db=SessionLocal(), questions_text=last_match.group().strip())
    return last_match.group().strip() if last_match else "No CreateQuestion content found."

async def fill(investment: float = 100.0, n_round: int = 2, summary: str = "", difficulty: str = "", num: str = "", label_1: str = "", label_2: str = ""):
    init = f"summary:{summary}\n\ndifficulty:{difficulty}\n\nnum:{num}\n\nlabel_1:{label_1}\n\nlabel_2:{label_2}"
    team = Team()
    team.hire([GetPdf(), Teacher1(), Reviewer()])
    team.invest(investment=investment)
    team.run_project(init)
    result = await team.run(n_round=n_round)

    pattern = re.compile(r'(?<=Teacher1:).*?(?=Reviewer:|$)', re.DOTALL)
    matches = pattern.finditer(result)
    last_match = next(matches, None)
    for match in matches:
        last_match = match

    if last_match:
        add_question_to_db(db=SessionLocal(), questions_text=last_match.group().strip())
    return last_match.group().strip() if last_match else "No CreateQuestion content found."

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        # 只有当创建的是文件时才处理
        if not event.is_directory:
            # 构建完整的文件路径
            file_path = event.src_path

            time.sleep(1)
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            parser = argparse.ArgumentParser(description='Generate exam questions from a PDF.')
            parser.add_argument('--filename', required=True, help='The PDF file to process.')
            parser.add_argument('--type', required=True, choices=['choice', 'judgement', 'fill'], help='The type of question to generate.')
            parser.add_argument('--difficulty', required=True, help='The difficulty level of the questions.')
            parser.add_argument('--num', required=True, type=int, help='The number of questions to generate.')
            parser.add_argument('--label_1', required=True, help='Label 1 for the questions.')
            parser.add_argument('--label_2', required=True, help='Label 2 for the questions.')
            args_list = shlex.split(content)
            args = parser.parse_args(args_list)
            pdf_text = asyncio.run(read_pdf_all_pages(args.filename))
            summary_result = asyncio.run(process_pdf_and_simulate(pdf_text))
            if args.type == 'choice':
                result = asyncio.run(choice(summary=summary_result, difficulty=args.difficulty, num=args.num, label_1=args.label_1, label_2=args.label_2))
            elif args.type == 'judgement':
                result = asyncio.run(judgement(summary=summary_result, difficulty=args.difficulty, num=args.num, label_1=args.label_1, label_2=args.label_2))
            elif args.type == 'fill':
                result = asyncio.run(fill(summary=summary_result, difficulty=args.difficulty, num=args.num, label_1=args.label_1, label_2=args.label_2))

            print(f"Processed PDF: {args.filename}")
            print(f"Question generation result:\n{result}")

                
            # 构建目标文件路径
            dest_path = os.path.join(dest_folder, os.path.basename(file_path))
            # 将内容写入目标文件夹
            with open(dest_path, 'w', encoding='utf-8') as file:
                file.write(result)
            # 删除原文件
            os.remove(file_path)
            print(f"Processed and moved: {file_path} to {dest_path}")

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, watch_folder, recursive=False)
    observer.start()
    try:
        while True:
            # 设置一个简单的循环，以便观察者可以在后台运行
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()