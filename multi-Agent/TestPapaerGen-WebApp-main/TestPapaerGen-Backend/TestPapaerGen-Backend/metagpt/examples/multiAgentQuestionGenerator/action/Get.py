from metagpt.actions import Action


class Get(Action):
    PROMPT_TEMPLATE: str = """
    直接输出{instruction}
    你的输出：
    """

    name: str = "Get"

    async def run(self, instruction: str):
        rsp = instruction
        return rsp
