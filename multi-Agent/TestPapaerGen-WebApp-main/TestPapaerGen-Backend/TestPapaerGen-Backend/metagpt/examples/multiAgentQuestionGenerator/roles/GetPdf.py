from examples.multiAgentQuestionGenerator.action.Get import Get
from metagpt.logs import logger
from metagpt.roles import Role
from metagpt.schema import Message


class GetPdf(Role):
    name: str = "Get"
    profile: str = "GetPdf"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([Get()])

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo  # todo will be SimpleWriteCode()
        msg = self.get_memories(k=1)[0]  # find the most recent messages
        code_text = await todo.run(msg.content)
        msg = Message(content=code_text, role=self.profile, cause_by=type(todo))
        return msg
