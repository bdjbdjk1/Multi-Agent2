import asyncio
import re
import string

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, Text, String, Numeric
from sqlalchemy.orm import Session

# 设置数据库连接
DATABASE_URL = "mysql+pymysql://root:ROOT@localhost/test_paper_generation"
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
    label_1 = Column(String(255), nullable=False)
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
            label_1 = None
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
                    label_1 = part.replace('次章节来源：', '').strip()

            if all([topic, answer, topic_type, score is not None, difficulty is not None]):
                new_question = Question(topic=topic, answer=answer, topic_type=topic_type, score=score,
                                        difficulty=difficulty, chapter_1=chapter_1, label_1=label_1, label_2=label_2)
                session.add(new_question)

        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()

# 使用函数
if __name__ == "__main__":
    # 创建数据库会话
    db = SessionLocal()

    # 准备数据
    question_data="""
题目：进程的同步与互斥是由于程序的（）引起的。
答案：D.并发执行
答案解释：进程的同步与互斥问题是由于程序的并发执行引起的。当多个进程或线程并发执行时，它们可能需要访问共享资源或共享数据，这就可能导致竞争条件。
题目类型：选择题
分数：2
难度：1
主章节来源：1
次章节来源：1.2
++++++
题目：在计算机网络中，什么是TCP/IP协议？
答案：TCP/IP协议是一组用于互联网和其他类似网络的通信协议。
答案解释：TCP/IP协议是传输控制协议/因特网互联协议，它定义了电子设备如何在网络上进行通信。
题目类型：问答题
分数：3
难度：2
主章节来源：2
次章节来源：2.1
"""

    # 将问题添加到数据库
    add_question_to_db(db, question_data)

    # 关闭会话
    db.close()
