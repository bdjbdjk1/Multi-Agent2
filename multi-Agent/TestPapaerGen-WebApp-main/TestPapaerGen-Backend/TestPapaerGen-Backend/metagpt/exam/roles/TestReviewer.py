# 定义审核者角色类
from metagpt.logs import logger
from metagpt.roles import Role
from metagpt.schema import Message
from exam.actions.CreatChoose import Choose
from exam.actions.ChecktTest import Checktest

class Reviewer(Role):
    name: str = "zhangsan"
    profile: str = "Reviewer"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([Checktest])  # 审核者角色执行检查题目的动作
        self._watch([Choose()])  # 监听生成题目的动作

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: ready to {self.rc.todo}")  # 记录日志
        todo = self.rc.todo

        msg = self.get_memories()[-1].content  # 获取历史记忆
        test_check = await Checktest().run(msg)  # 调用检查题目的动作
        logger.info(f'reviewer: {test_check}')  # 记录检查结果
        msg = Message(content=test_check, role=self.profile, cause_by=type(todo))  # 创建消息对象
        return msg
