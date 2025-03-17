from exam.actions.generate import GenerateQuestion
from exam.actions.pdfchange import Summarize
from metagpt.const import MESSAGE_ROUTE_TO_ALL
from metagpt.logs import logger
from metagpt.roles import Role
from metagpt.schema import Message

class Teacher(Role):
    name: str = "llm"
    profile: str ="Teacher"
    def __init__(self, **kwargs):
      super().__init__(**kwargs)
      self.set_actions([GenerateQuestion])  
      self._watch([Summarize])  
    async def _act(self) -> Message:
        logger.info(f"{self._setting}: ready to {self.rc.todo}")
        todo = self.rc.todo

        msg = self.get_memories()[1]
        subject=self.get_memories()[1]
        num_questions = 1  # 题目数量
        questions_text= await GenerateQuestion().run(msg, subject, num_questions)  # 调用生成题目的动作
        logger.info(f'teacher: {questions_text}')  # 记录生成的题目
        msg = Message(topic=questions_text, role=self.profile, cause_by=type(todo))  # 创建消息对象
        return msg