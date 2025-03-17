
from exam.actions.pdfchange import Summarize
from exam.actions.ChecktTest import CheckDuplicate
from exam.actions.CreatJudge import Judge
from metagpt.const import MESSAGE_ROUTE_TO_ALL
from metagpt.logs import logger
from metagpt.roles import Role
from metagpt.schema import Message

class Teacher2(Role):
    name: str = "llm"
    profile: str ="Teacher2"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([Judge])
        self._watch([Summarize, CheckDuplicate])

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

        questions_text = await Judge().run(subject, num_questions, check)  # 调用生成题目的动作
        logger.info(f'teacher: {questions_text}')  # 记录生成的题目
        msg = Message(content=questions_text, role=self.profile, cause_by=type(todo))
        return msg
