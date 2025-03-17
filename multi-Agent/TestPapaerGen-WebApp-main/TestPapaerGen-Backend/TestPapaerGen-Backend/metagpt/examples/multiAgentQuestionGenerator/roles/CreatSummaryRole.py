from examples.multiAgentQuestionGenerator.action.CheckSummary import CheckSummary
from examples.multiAgentQuestionGenerator.action.CreateSummary import CreateSummary
from examples.multiAgentQuestionGenerator.action.Read import Read
from metagpt.logs import logger
from metagpt.roles import Role
from metagpt.schema import Message


class CreateSummaryRole(Role):
    name: str = "Alice"
    profile: str = "CreateSummaryRole"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([CreateSummary()])
        self._watch([CheckSummary(), Read()])

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo  # todo will be SimpleWriteCode()
        records = self.get_memories()
        if len(records) >= 3:
            check = self.get_memories(k=1)[0]
        else:
            check = None
        print("正在读取检查信息...............")
        print("check:" + str(check))
        msg = self.get_memories(-1)[0]
        print("正在读取文本信息...............")
        logger.info("生成知识点摘要中...")
        code_text = await todo.run(msg.content, check)
        msg = Message(content=code_text, role=self.profile, cause_by=type(todo))
        logger.info("知识点摘要生成完成")
        return msg
