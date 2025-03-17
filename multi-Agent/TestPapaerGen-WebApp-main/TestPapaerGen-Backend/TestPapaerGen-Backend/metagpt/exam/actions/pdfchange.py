import re
from metagpt.actions import Action

# 定义概括文本的动作类
class Summarize(Action):
    PROMPT_TEMPLATE: str = """
    你是一位概括文档方面的专家你需要帮我完成一下的任务
    概括{instruction}为300字的文字
    你的概括：
    """

    name: str = "Summarize"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)
        rsp = await self._aask(prompt)
        return rsp


