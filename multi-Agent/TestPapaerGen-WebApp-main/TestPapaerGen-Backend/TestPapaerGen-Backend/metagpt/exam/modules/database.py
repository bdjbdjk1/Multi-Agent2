# /exam/modules/models.py
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, Text, String, Numeric

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
#Base.metadata.create_all(bind=engine)