from exam.actions.pdfchange import Summarize
from metagpt.logs import logger
from metagpt.roles import Role
from metagpt.schema import Message

class PdfReader(Role):
    name: str = "Alice"
    profile: str = "PdfReader"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([Summarize])
        
    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo

        context = self.get_memories(k=1)[0]  # find the most recent messages
        code_text = await todo.run(context)
        msg = Message(content=code_text, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)
        return msg