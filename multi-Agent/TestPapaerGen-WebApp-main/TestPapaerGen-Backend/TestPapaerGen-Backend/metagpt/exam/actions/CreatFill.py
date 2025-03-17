from metagpt.actions import Action
from metagpt.logs import logger


class Fill(Action):
    name: str = "Fill"

    # 生成题目的提示模板
    PROMPT_TEMPLATE: str = """
#角色
生成填空题题目的专家

#语言
中文

#描述
根据{subject}的书本知识点内容，生成填空题考试题目，并输出主章节和此章节标识，题目数量为{num_questions}。

#目标
##需要生成题目，题目选项，正确答案，答案解释，题目类型，主章节来源，次章节来源，分数和难度9个部分。
##章节定义：必须根据{subject}的内容准确识别生成的题目所属知识点主、次章节来源。
##难度定义：布鲁姆分类法的记忆、理解、应用、分析、评价、创造六个层面分别对于难度1，2，3，4，5，6
##分数定义：布鲁姆分类法的一、二层次对应于分数2分，三层次对应于分数3分，四层次对应于分数4分，五层次对应于分数5分，六层次对应于分数6分
##答案解释：解释需要有{subject}的知识点内容作为支撑，不能随意生成。


# 约束
##分数输出格式类似于：1；难度输出格式类似于：1；大章节输出格式类似于：1；次章节输出格式类似于：1.1；
##格式：必须在每个题目之间输出“++++++”，“++++++”是每个题目之间的分隔符，尤为重要
##严格按照示例中的<正向示例>示例格式进行输出。不能把<示例>中的例子直接作为输出内容，只能参考<示例>中输出的格式
##生成的题目必须为陈述句，题目中的下划线部分为需要填入的选项内容，位置可以任意。
##不需要输出“请注意，这些题目主要针对布鲁姆分类法的前两个层次（知识、理解），适合用于初步考察学生对操作系统基本概念和原理的掌握。”等提示


## 示例
<正向示例>
题目：
分时系统的基本特征是__、__、__。
++++++
答案：同时性 多路性 交互性
答案解释：分时系统的基本特征包括同时性、多路性和交互性，而独立性并不是分时系统的基本特征。
题目类型：填空
分数：2
难度：1
主章节来源：1
次章节来源：3.2
++++++
++++++
    
生成题目:

    """

    async def run(self, subject: str, num_questions: int, check: str):
        # 运行生成题目的方法
        logger.info(f'Starting to generate questions for subject "{subject}" .')
        prompt = self.PROMPT_TEMPLATE.format(subject=subject, num_questions=num_questions, check=check)
        rsp = await self._aask(prompt)  # 使用内部方法进行交互
        logger.info(f'Finished generating questions for subject "{subject}".')
        return rsp
