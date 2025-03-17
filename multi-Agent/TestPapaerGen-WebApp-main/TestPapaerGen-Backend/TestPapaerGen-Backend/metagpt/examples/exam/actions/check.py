from metagpt.actions import Action

# 定义检查重复题目的动作类
class CheckDuplicate(Action):
    name: str = "CheckDuplicate"

    # 检查重复题目的提示模板
    PROMPT_TEMPLATE: str = """
    这是历史对话记录：{msg}。
    请检查生成的考试题目是否重复。只返回重复题目的列表，不包含其他文本。
    重复的题目：
    """

    async def run(self, msg: str):
        # 运行检查重复题目的方法
        prompt = self.PROMPT_TEMPLATE.format(msg=msg)
        rsp = await self._aask(prompt)  #令LLM 赋予这个动作能力
        return rsp