import asyncio
from concurrent.futures import ThreadPoolExecutor
import pdfplumber
import typer
from metagpt.logs import logger
from metagpt.team import Team
from exam.roles.pdf_reader import PdfReader
from exam.roles.TestReviewer import Reviewer
from exam.roles.CreatChooseRole import Teacher
app = typer.Typer()

executor = ThreadPoolExecutor(max_workers=1)  # 创建线程池
# 固定的PDF文件路径
fixed_pdf_path = 'E:\MetaGPT\examples\多智能体测试\基于智能体的试卷生成系统.pdf'

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
    n_round: int = typer.Option(default=5, help="Number of rounds for the simulation."),
):
    logger.info(f"Processing PDF at {fixed_pdf_path}")

    # 异步读取PDF
    loop = asyncio.get_event_loop()
    pdf_text = loop.run_until_complete(read_pdf_all_pages(fixed_pdf_path))

    # 创建团队并雇佣智能体
    team = Team()
    team.hire([PdfReader(), Teacher(),Reviewer()])
    team.run_project(pdf_text)

    # 运行多轮模拟
    loop.run_until_complete(team.run(n_round=n_round))


if __name__ == '__main__':
    typer.run(main)