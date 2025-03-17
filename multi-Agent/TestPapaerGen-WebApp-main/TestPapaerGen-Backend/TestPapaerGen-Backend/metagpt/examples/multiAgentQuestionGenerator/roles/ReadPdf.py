from examples.multiAgentQuestionGenerator.action.Read import Read
from metagpt.logs import logger
from metagpt.roles import Role
from metagpt.schema import Message


class ReadPdf(Role):
    name: str = "Read"
    profile: str = "ReadPdf"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([Read()])

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo  # todo will be SimpleWriteCode()
        msg = self.get_memories(k=1)[0]  # find the most recent messages
        code_text = await todo.run(msg.content)
        msg = Message(content=code_text, role=self.profile, cause_by=type(todo))
        return msg
