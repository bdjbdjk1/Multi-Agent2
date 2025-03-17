# 定义审核者角色类
from metagpt.logs import logger
from metagpt.roles import Role
from metagpt.schema import Message
from exam.actions.generate import GenerateQuestion
from exam.actions.ChecktTest import CheckDuplicate
from exam.actions.pdfchange import Summarize

class Reviewer(Role):
    name: str = "zhangsan"
    profile: str = "Reviewer"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([CheckDuplicate])  # 设置审核者角色可以执行检查重复题目的动作
        self._watch([GenerateQuestion])  # 监听生成题目的动作

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: ready to {self.rc.todo}")  # 记录日志
        todo = self.rc.todo

        previous_question = self.get_memories()
        duplicate_check = await self.CheckDuplicate().run(previous_question)  # 调用检查重复题目的动作
        logger.info(f'reviewer: {duplicate_check}')  # 记录重复题目的检查结果
        msg = Message(topic=duplicate_check, role=self.profile, cause_by=type(todo))  # 创建消息对象
        return msg
