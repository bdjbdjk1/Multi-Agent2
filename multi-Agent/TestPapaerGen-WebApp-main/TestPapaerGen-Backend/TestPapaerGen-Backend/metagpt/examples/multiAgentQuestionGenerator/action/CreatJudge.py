from metagpt.actions import Action
from metagpt.logs import logger


class Judge(Action):
    name: str = "Judge"

    # 生成题目的提示模板
    PROMPT_TEMPLATE: str = """
#角色
生成判断题题目的专家

#语言
中文

#描述
根据{summary_content}的书本知识点内容，生成判断题考试题目，主章节为{label_1_content}和次章节为{label_2_content}，题目数量为{num_content}，题目难度为{difficulty_content}。

#目标
##需要生成题题目，题目选项，正确答案，答案解释，题目类型，主章节来源，次章节来源，分数和难度9个部分。
##章节定义：必须根据{summary_content}的内容准确识别生成所属知识点来源主要章节为{label_1_content}、次章节为{label_2_content}的题目。
##难度定义：布鲁姆分类法的记忆、理解、应用、分析、评价、创造六个层面分别对于难度1，2，3，4，5，6
##分数定义：布鲁姆分类法的一、二层次对应于分数2分，三层次对应于分数3分，四层次对应于分数4分，五层次对应于分数5分，六层次对应于分数6分
##答案解释：解释需要有{summary_content}的知识点内容作为支撑，不能随意生成。


# 约束
##分数输出格式类似于：1；难度输出格式类似于：1；大章节输出格式类似于：1；次章节输出格式类似于：1.1；
##格式：必须在每个题目之间输出“++++++”，“++++++”是每个题目之间的分隔符，尤为重要
##严格按照示例中的<正向示例>示例格式进行输出。不能把<示例>中的例子直接作为输出内容，只能参考<示例>中输出的格式
##生成的题目必须为陈述句，题目中的空格部分需要填入‘对’或者‘错’，空格位置在最后。
##不需要输出“请注意，这些题目主要针对布鲁姆分类法的前两个层次（知识、理解），适合用于初步考察学生对操作系统基本概念和原理的掌握。”等提示
##你必须输出每道题中类似：“题目：”、“答案：”、“答案解释：”、“题目类型：”这样的标志
##生成所属知识点主要章节为{label_1_content}、次章节为{label_2_content}的题目
##生成题目难度为{difficulty_content}的题目

## 示例
<正向示例>
题目：进程的同步与互斥是由于程序的并发执行引起的。（）
答案：对
答案解释：进程的同步与互斥问题是由于程序的并发执行引起的。当多个进程或线程并发执行时，它们可能需要访问共享资源或共享数据，这就可能导致竞争条件。
题目类型：判断题
分数：2
难度：2
主章节来源：3
次章节来源：3.1
++++++
    
生成题目:

    """

    async def run(self, summary_content: str, difficulty_content: str, num_content: str, label_1_content: str,
                  label_2_content: str, check: str):
        logger.info(f'Starting to generate questions for summary_content "{summary_content}" .')
        prompt = self.PROMPT_TEMPLATE.format(summary_content=summary_content, difficulty_content=difficulty_content,
                                             num_content=num_content, label_1_content=label_1_content,
                                             label_2_content=label_2_content, check=check)
        rsp = await self._aask(prompt)  # 使用内部方法进行交互
        logger.info(f'Finished generating questions for summary_content "{summary_content}".')
        return rsp
