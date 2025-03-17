from metagpt.actions import Action
from metagpt.logs import logger


class GenerateQuestion(Action):
    name: str = "GenerateQuestion"

    # 生成题目的提示模板
    PROMPT_TEMPLATE: str = """
难度定义：布鲁姆分类法的知道、领会、应用、分析、综合、评价六个层面分别对于难度1，2，3，4，5，6
概要为{subject}的知识点
生成{num_questions}道考试题目。
这是你的检查结果，第一次可能和概要一样{check},请按照结果进行合适的修改
需要生成题目，题目答案，题目类型，分数和难度5个部分。
限制：分数输出格式类似于：1；难度输出格式类似于：1；
不需要输出“请注意，这些题目主要针对布鲁姆分类法的前两个层次（知识、理解），适合用于初步考察学生对操作系统基本概念和原理的掌握。”等提示
输出格式为

题目：什么是操作系统？请简述其主要功能。
答案：操作系统是管理计算机硬件和软件资源的系统软件，主要功能包括进程管理、内存管理、文件系统、输入/输出管理和用户接口等。
题目类型：选择题
分数：2
难度：1
++++++
必须在每个题目之间输出“++++++”，“++++++”是每个题目之间的分隔符，尤为重要
你的题目：
    """

    async def run(self, msg: str, subject: str, num_questions: int, check: str):
        # 运行生成题目的方法
        logger.info(f'Starting to generate questions for subject "{subject}" with message "{msg}".')
        prompt = self.PROMPT_TEMPLATE.format(msg=msg, subject=subject, num_questions=num_questions, check=check)
        rsp = await self._aask(prompt)  # 使用内部方法进行交互
        logger.info(f'Finished generating questions for subject "{subject}".')
        return rsp
