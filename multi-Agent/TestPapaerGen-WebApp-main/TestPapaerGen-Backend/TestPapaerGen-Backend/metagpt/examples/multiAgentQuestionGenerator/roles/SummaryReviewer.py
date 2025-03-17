from examples.multiAgentQuestionGenerator.action.CheckSummary import CheckSummary
from examples.multiAgentQuestionGenerator.roles.CreatSummaryRole import CreateSummary
from metagpt.logs import logger
from metagpt.roles import Role
from metagpt.schema import Message


class SummaryReviewer(Role):
    name: str = "bot2"
    profile: str = "SummaryReviewer"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([CheckSummary()])  # 设置审核者角色可以执行检查重复题目的动作
        self._watch([CreateSummary()])  # 监听生成题目的动作

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: ready to {self.rc.todo}")  # 记录日志
        todo = self.rc.todo

        # 在获取历史记忆前记录
        logger.info("Fetching the latest memory...")

        memories = self.get_memories()
        if not memories:
            logger.warning("No memories found.")
            return Message(content="No memories available.", role=self.profile, cause_by=type(todo))

        # 在获取历史记忆后记录
        logger.info("Latest memory fetched successfully.")

        msg = memories[-1].content  # 获取历史记忆
        print("知识点：" + str(msg))
        duplicate_check = await CheckSummary().run(msg)
        logger.info(f'Duplicate check completed: {duplicate_check}')
        msg = Message(content=duplicate_check, role=self.profile, cause_by=type(todo))  # 创建消息对象

        return msg
