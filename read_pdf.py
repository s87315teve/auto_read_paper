import os
from PyPDF2 import PdfReader

def read_pdf(file_path):
    """讀取PDF文件並返回其文字內容"""
    with open(file_path, 'rb') as file:
        pdf = PdfReader(file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def process_text(text):
    """處理文字的函數"""
    # 這裡是您想要處理文字的邏輯
    # 例如,我們可以簡單地計算字數
    word_count = len(text.split())
    # print(text)
    return f"文件包含 {word_count} 個字"


def process_pdf_folder(folder_path):
    """處理指定資料夾中的所有PDF文件"""
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            print(f"正在處理: {filename}")
            text = read_pdf(file_path)
            result = process_text(text)
            print(result)
            print("-------------------")

# 主程式
if __name__ == "__main__":
    # folder_path = input("請輸入PDF文件所在的資料夾路徑: ")
    folder_path="D:\\research\ICC 2024-20240814T062802Z-001\\ICC 2024\\papers"
    process_pdf_folder(folder_path)