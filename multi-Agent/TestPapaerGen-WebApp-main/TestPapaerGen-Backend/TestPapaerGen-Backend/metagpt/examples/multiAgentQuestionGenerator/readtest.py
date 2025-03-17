import asyncio
import re
import string
from concurrent.futures import ThreadPoolExecutor

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

# 设置数据库连接
# 设置数据库连接
DATABASE_URL = "mysql+pymysql://root:linmei040522.@cd-cdb-7bcbz5hc.sql.tencentcdb.com:29116/test"
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
    # 实例化Question模型
    session = SessionLocal()
    try:
        # 将题目文本分割成单个题目
        questions = questions_text.split('++++++')  # 这里需要一个明确的分隔符来区分不同的题目

        for question_text in questions:
            if not question_text.strip():
                continue

            # 解析每个题目
            parts = question_text.split('\n')
            topic = None
            answer = None
            topic_type = None
            score = None
            difficulty = None
            chapter_1 = None
            chapter_2 = None
            label_2 = None

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
                new_question = Question(topic=topic, answer=answer, topic_type=topic_type, score=score,
                                        difficulty=difficulty, chapter_1=chapter_1, chapter_2=chapter_2,
                                        label_2=label_2)
                session.add(new_question)

        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()


# Base.metadata.create_all(bind=engine)


executor = ThreadPoolExecutor(max_workers=1)  # 创建线程池

# 固定的PDF文件路径
fixed_pdf_path = '基于智能体的试卷生成系统.pdf'


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


async def process_pdf_and_simulate(investment: float = 100.0, n_round: int = 2):
    # 异步读取PDF
    pdf_text = await read_pdf_all_pages(fixed_pdf_path)  # 假设read_pdf_all_pages是一个异步函数

    # 创建团队并雇佣智能体
    team = Team()
    team.hire([ReadPdf(), CreateSummaryRole(), SummaryReviewer()])

    # 投资和启动项目
    team.invest(investment=investment)
    team.run_project(pdf_text)

    # 运行多轮模拟
    result = await team.run(n_round=n_round)  # 假设team.run是一个异步函数

    print(result)

    # 处理结果
    pattern = re.compile(r'(?<=CreateSummaryRole:).*?(?=SummaryReviewer:|$)', re.DOTALL)
    matches = pattern.finditer(result)
    last_match = next(matches, None)
    for match in matches:
        last_match = match
    if last_match:
        print("这是生成概要的结果：" + last_match.group().strip())
    else:
        print("No CreateQuestion content found.")

    return last_match.group().strip() if last_match else ""


async def question(investment: float = 100.0, n_round: int = 2, init: str = ""):
    # 创建团队并雇佣智能体
    team = Team()
    team.hire([GetPdf(), Teacher(), Reviewer()])

    # 投资和启动项目
    team.invest(investment=investment)
    team.run_project(init)

    # 运行多轮模拟
    result = await team.run(n_round=n_round)  # 假设team.run是一个异步函数
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    pattern = re.compile(r'(?<=Teacher:).*?(?=Reviewer:|$)', re.DOTALL)
    matches = pattern.finditer(result)
    last_match = next(matches, None)
    for match in matches:
        last_match = match

    if last_match:
        print("这是生成的题目：" + last_match.group().strip())
    else:
        print("No CreateQuestion content found.")
    add_question_to_db(db=SessionLocal(), questions_text=last_match.group().strip())
    return last_match.group().strip()


async def judgement(investment: float = 100.0, n_round: int = 2, init: str = ""):
    # 创建团队并雇佣智能体
    team = Team()
    team.hire([GetPdf(), Teacher2(), Reviewer()])

    # 投资和启动项目
    team.invest(investment=investment)
    team.run_project(init)

    # 运行多轮模拟
    result = await team.run(n_round=n_round)  # 假设team.run是一个异步函数
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    pattern = re.compile(r'(?<=Teacher2:).*?(?=Reviewer:|$)', re.DOTALL)
    matches = pattern.finditer(result)
    last_match = next(matches, None)
    for match in matches:
        last_match = match

    if last_match:
        print("这是生成的题目：" + last_match.group().strip())
    else:
        print("No CreateQuestion content found.")
    add_question_to_db(db=SessionLocal(), questions_text=last_match.group().strip())
    return last_match.group().strip()


async def fill(investment: float = 100.0, n_round: int = 2, init: str = ""):
    # 创建团队并雇佣智能体
    team = Team()
    team.hire([GetPdf(), Teacher1(), Reviewer()])

    # 投资和启动项目
    team.invest(investment=investment)
    team.run_project(init)

    # 运行多轮模拟
    result = await team.run(n_round=n_round)  # 假设team.run是一个异步函数
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    pattern = re.compile(r'(?<=Teacher1:).*?(?=Reviewer:|$)', re.DOTALL)
    matches = pattern.finditer(result)
    last_match = next(matches, None)
    for match in matches:
        last_match = match

    if last_match:
        print("这是生成的题目：" + last_match.group().strip())
    else:
        print("No CreateQuestion content found.")
    add_question_to_db(db=SessionLocal(), questions_text=last_match.group().strip())
    return last_match.group().strip()


async def main():
    simulate_result = """第一章：基于多智能体的试卷生成系统概述
1.1 信息技术对教育领域的影响
知识点：
- 信息技术的发展推动了教育领域的变革，智能教育系统成为现代教育体系中的重要组成部分。
- 试卷作为衡量学生学习成果和评估教学质量的重要手段，在传统生成方式中存在效率低下和质量波动等问题。

1.2 基于多智能体的试卷生成系统的意义
知识点：
- 该系统利用多智能体技术，通过智能算法和数据分析，自动完成试卷生成工作，提高生成效率和质量。
- 系统可以根据教师需求和学生学习情况，快速生成符合要求的试卷，为教学评估提供支持。
- 系统通过预设规则和算法，确保每次生成的试卷符合质量标准，避免质量波动问题。
- 系统可以根据学生反馈和表现，不断优化生成的试卷，使其更贴近学生实际需求。"""
    # 正确地调用 question 函数并等待其完成
    question_result = await fill(init=simulate_result)


# 运行主函数
if __name__ == "__main__":
    asyncio.run(main())
