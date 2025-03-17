import os
import asyncio
from flask import Flask, render_template, request, jsonify
from concurrent.futures import ThreadPoolExecutor
from metagpt.logs import logger
import pdfplumber
from metagpt.team import Team
from exam.roles.pdf_reader import PdfReader
from exam.roles.TestReviewer import Reviewer
from exam.roles.CreatChooseRole import Teacher

# 创建Flask应用实例
app = Flask(__name__)

executor = ThreadPoolExecutor(max_workers=1)  # 创建线程池

# Flask应用实例
flask_app = Flask(__name__)
@app.route('/list_pdfs')
def list_pdfs():
    directory = 'E:\MetaGPT\exam\web'
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    return jsonify(pdf_files)

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
# 定义主页路由
@app.route('/')
def index():
    return render_template('test1.html')


# 定义处理表单数据的路由
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        user_input = request.form['user_input']
        return f"你输入的内容是: {user_input}"
    else:
        return "错误：此页面仅接受POST请求。"


@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join("E:\MetaGPT\exam\web",
                                 uploaded_file.filename)
        uploaded_file.save(file_path)
        return f"文件已成功上传至 {file_path}"
    else:
        return "没有选择文件进行上传。"


@app.route('/process_pdf', methods=['GET'])
def process_pdf():
    try:
        # 从请求中获取参数
        pdf_path = request.args.get('pdf_path')  # 新增：获取文件路径参数
        investment = float(request.args.get('investment', 100.0))
        n_round = int(request.args.get('n_round', 5))

        # 异步读取PDF
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        pdf_text = loop.run_until_complete(read_pdf_all_pages("E:/MetaGPT/exam/web/"+pdf_path))  # 使用新的pdf_path

        # 创建团队并雇佣智能体
        team = Team()
        team.hire([PdfReader(), Teacher(), Reviewer()])

        # 投资和启动项目
        team.invest(investment=investment)
        team.run_project(pdf_text)

        # 运行多轮模拟
        result = loop.run_until_complete(team.run(n_round=n_round))

        # 关闭事件循环
        loop.close()

        return jsonify({"status": "success", "result": result})
    except Exception as e:
        logger.error(f"Error processing PDF: {e}")
        return jsonify({"status": "error", "message": str(e)})

# 主程序入口
if __name__ == '__main__':
    app.run(debug=True)