from metagpt.actions import Action


class Read(Action):
    PROMPT_TEMPLATE: str = """
    直接输出{instruction}
    你的输出：
    """

    name: str = "Read"

    async def run(self, instruction: str):
        rsp = instruction
        return rsp
