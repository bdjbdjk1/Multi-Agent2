from metagpt.actions import Action

# 定义检查题目的动作类
class Checktest(Action):
    name: str = "Checktest"

    # 检查重复题目的提示模板
    PROMPT_TEMPLATE: str = """
    #角色
    审查题目的审核者

    #语言
    中文

    #描述
    根据{msg}的知识点内容，审核生成题目的答案是否正确，以及章节是否归纳正确，难度定义是否正确。
    #目标
    ##章节检查：必须根据{msg}的内容准确审核生成的题目所属知识点主、次章节来源，不正确则给出修改建议。
    ##难度检查：布鲁姆分类法的记忆、理解、应用、分析、评价、创造六个层面分别对于难度1，2，3，4，5，6，审核题目的真实难度是否达到了标注的难度层次，不合理给出修改建议。
    ##答案检查：
    检查题目答案是否正确，不正确给出修改建议

    """
    async def run(self, msg: str):
        # 运行检查题目的方法
        prompt = self.PROMPT_TEMPLATE.format(msg=msg)
        rsp = await self._aask(prompt)  #令LLM 赋予这个动作能力
        return rsp