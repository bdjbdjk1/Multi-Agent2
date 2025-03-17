import re

from examples.multiAgentQuestionGenerator.action.ChecktTest import Checktest
from examples.multiAgentQuestionGenerator.action.CreatJudge import Judge
from examples.multiAgentQuestionGenerator.action.Get import Get
from metagpt.const import MESSAGE_ROUTE_TO_ALL
from metagpt.logs import logger
from metagpt.roles import Role
from metagpt.schema import Message


class Teacher2(Role):
    name: str = "llm"
    profile: str = "Teacher2"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([Judge])
        self._watch([Get, Checktest])

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: ready to {self.rc.todo}")  # 记录日志

        todo = self.rc.todo

        check = self.get_memories()[1].content  # 检查结果反馈
        if len(self.get_memories()) >= 3:

            check = self.get_memories()[1].content  # 检查结果反馈
        else:
            check = None
        print("check:" + str(check))

        init = self.get_memories()[-1].content  # 内容来源
        summary_match = re.search(r'summary:(.*?)(?=difficulty:)', init, re.DOTALL)
        summary_content = summary_match.group(1).strip() if summary_match else None

        # 提取 difficulty 内容
        difficulty_match = re.search(r'difficulty:(\d+)', init)
        difficulty_content = difficulty_match.group(1) if difficulty_match else None

        # 提取 num 内容
        num_match = re.search(r'num:(\d+)', init)
        num_content = num_match.group(1) if num_match else None

        # 提取 label_1 内容
        label_1_match = re.search(r'label_1:(\d+)', init)
        label_1_content = label_1_match.group(1) if label_1_match else None

        # 提取 label_2 内容
        label_2_match = re.search(r'label_2:(\d+\.\d+)', init)
        label_2_content = label_2_match.group(1) if label_2_match else None
        print("++++++++++++++++++++++++++")
        print("Summary content:", summary_content)
        print("Difficulty:", difficulty_content)
        print("Num:", num_content)
        print("Label 1:", label_1_content)
        print("Label 2:", label_2_content)

        print("正在读取生成的科目摘要...............")
        questions_text = await Judge().run(summary_content, difficulty_content, num_content, label_1_content,
                                           label_2_content, check)

        logger.info(f'teacher1: {questions_text}')  # 记录生成的题目
        msg = Message(content=questions_text, role=self.profile, cause_by=type(todo))
        return msg
