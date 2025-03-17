# pdf_processor.py

import pdfplumber

def read_pdf_all_pages(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"  # 提取文本并添加换行符
    return text
