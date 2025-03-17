from exam.actions.CreatChoose import Choose
from exam.actions.pdfchange import Summarize
from exam.actions.ChecktTest import Checktest
from metagpt.const import MESSAGE_ROUTE_TO_ALL
from metagpt.logs import logger
from metagpt.roles import Role
from metagpt.schema import Message

class Teacher(Role):
    name: str = "llm"
    profile: str ="Teacher"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([Choose])
        self._watch([Summarize, Checktest])

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: ready to {self.rc.todo}")  # 记录日志
        todo = self.rc.todo
        num_questions = 10  # 指定生成题目的数量

        check = self.get_memories()[1].content #检查结果反馈
        if len(self.get_memories())>=2:

            check = self.get_memories()[1].content #检查结果反馈
        else:
            check=None
        print("check:" + str(check))
        subject = self.get_memories()[-1].content  # 内容来源
        print("正在读取生成的科目摘要...............")
        print("subject:" + str(subject))

        questions_text = await Choose().run(subject, num_questions, check)  # 调用生成题目的动作
        logger.info(f'teacher: {questions_text}')  # 记录生成的题目
        msg = Message(content=questions_text, role=self.profile, cause_by=type(todo))
        return msg
