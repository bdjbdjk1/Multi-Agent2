import asyncio
import re
from concurrent.futures import ThreadPoolExecutor
import typer

from examples.multiAgentQuestionGenerator.roles.CreatSummaryRole import CreateSummaryRole
from examples.multiAgentQuestionGenerator.roles.GetPdf import GetPdf
from examples.multiAgentQuestionGenerator.roles.ReadPdf import ReadPdf
from examples.multiAgentQuestionGenerator.roles.SummaryReviewer import SummaryReviewer
from examples.reverse_engineering import app

from metagpt.logs import logger
import pdfplumber
from metagpt.team import Team

executor = ThreadPoolExecutor(max_workers=1)  # 创建线程池

# 固定的PDF文件路径
fixed_pdf_path = '基于智能体的试卷生成系统.pdf'


async def read_pdf_all_pages(pdf_path):
    loop = asyncio.get_event_loop()
    text = await loop.run_in_executor(executor, lambda: _read_pdf_all_pages(pdf_path))
    return text


def _read_pdf_all_pages(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


@app.command()
def main(
        # pdf_path: str = typer.Argument(..., help="Path to the PDF file to process"),  # 原始参数定义
        investment: float = typer.Option(default=100.0, help="Dollar amount to invest in the AI company."),
        n_round: int = typer.Option(default=2, help="Number of rounds for the simulation."),
):
    logger.info(f"Processing PDF at {fixed_pdf_path}")
    # 异步读取PDF
    loop = asyncio.get_event_loop()
    pdf_text = loop.run_until_complete(read_pdf_all_pages(fixed_pdf_path))
    # 创建团队并雇佣智能体
    team = Team()
    team.hire([GetPdf()])
    # 投资和启动项目
    team.invest(investment=investment)
    team.run_project(pdf_text)
    # 运行多轮模拟
    result = loop.run_until_complete(team.run(n_round=n_round))
    loop.close()
    print(result)




if __name__ == '__main__':
    typer.run(main)
