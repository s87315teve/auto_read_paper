import os
import csv
from PyPDF2 import PdfReader
import ollama

# model_name="llama3.1:8b"
# model_name="llama3.1:8b-instruct-fp16"
# default model is llama3.1:8b
# can try llama3.1:8b-instruct-fp16 on RTX4090

def read_pdf(file_path):
    """讀取PDF檔案並返回其文字內容和標題"""
    with open(file_path, 'rb') as file:
        pdf = PdfReader(file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        title = pdf.metadata.get('/Title', 'Unknown Title')
        if title == 'Unknown Title':
            title = ' '.join(text.split()[:5]) + '...'
    return text, title

def classify_paper(text, categories):
    """使用LLM來對文本進行分類"""
    categories_str = ", ".join(categories)
    prompt = f"""
    請將以下文本分類到最合適的類別中。可用的類別有：{categories_str}

    回答格式：
    分類: [選擇的類別]
    理由: [你的解釋]

    請確保你的回答嚴格遵循上述格式。

    文本：{text[:1500]}...
    """
    response = ollama.chat(model=model_name, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

def parse_classification(response):
    """解析LLM的回應以確定分類結果"""
    lines = response.split('\n')
    category = None
    reason = ""
    for line in lines:
        if line.startswith("分類:"):
            category = line[3:].strip()
        elif line.startswith("理由:"):
            reason = line[3:].strip()
    return category, reason

def process_pdf_folder(folder_path, categories, csv_path):
    """處理指定資料夾中的所有PDF檔案，進行分類，並將結果寫入CSV"""
    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Filename', 'Title', 'Category', 'Reason'])
        
        for filename in os.listdir(folder_path):
            if filename.endswith(".pdf"):
                file_path = os.path.join(folder_path, filename)
                text, title = read_pdf(file_path)
                print(f"正在處理: {filename}")
                print(f"標題: {title}")
                classification_response = classify_paper(text, categories)
                category, reason = parse_classification(classification_response)
                print(f"分類: {category}")
                print(f"理由: {reason}")
                
                csv_writer.writerow([filename, title, category, reason])
                csvfile.flush()
                print("-------------------")

# 主程式
if __name__ == "__main__":
    folder_path = "../3dmap"
    categories = ["Tool", "Machine learning + wireless", "Wireless", "Survey", "Book", "Dynamic Transmission", "Sensor fusion", "Neural network architecture", "Standardization", "Air-to-ground channel", "Other"]
    csv_path = folder_path+"/paper_classification.csv"
    model_name="llama3.1:8b"
    
    print(f"分類類別: {', '.join(categories)}")
    process_pdf_folder(folder_path, categories, csv_path)
    
    print(f"\n所有論文的分類結果已儲存至 {csv_path}")