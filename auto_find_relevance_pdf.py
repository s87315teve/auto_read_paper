import os
import csv
from PyPDF2 import PdfReader
import ollama

def read_pdf(file_path):
    """讀取PDF文件並返回其文字內容和標題"""
    with open(file_path, 'rb') as file:
        pdf = PdfReader(file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        title = pdf.metadata.get('/Title', 'Unknown Title')
        if title == 'Unknown Title':
            title = ' '.join(text.split()[:5]) + '...'
    return text, title

def is_relevant(text, topic):
    """使用LLM來判斷文本是否與主題相關"""
    prompt = f"""
    請判斷以下文本是否與主題 "{topic}" 相關。
    
    回答格式：
    相關性: [是/否]
    理由: [你的解釋]
    
    請確保你的回答嚴格遵循上述格式。

    文本：{text[:1500]}...
    """
    response = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

def parse_relevance(response):
    """解析LLM的回應以確定相關性"""
    lines = response.split('\n')
    relevance = None
    reason = ""
    for line in lines:
        if line.startswith("相關性:"):
            relevance = "是" if "是" in line else "否"
        elif line.startswith("理由:"):
            reason = line[3:].strip()
    return relevance, reason

def process_pdf_folder(folder_path, topic, csv_path):
    """處理指定資料夾中的所有PDF文件，找出與主題相關的論文，並將結果寫入CSV"""
    relevant_papers = []
    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Filename', 'Title', 'Relevance', 'Reason'])
        
        for filename in os.listdir(folder_path):
            if filename.endswith(".pdf"):
                file_path = os.path.join(folder_path, filename)
                text, title = read_pdf(file_path)
                print(f"正在處理: {filename}")
                print(f"標題: {title}")
                relevance_response = is_relevant(text, topic)
                relevance, reason = parse_relevance(relevance_response)
                print(f"相關性: {relevance}")
                print(f"理由: {reason}")
                
                csv_writer.writerow([filename, title, relevance, reason])
                csvfile.flush()
                
                if relevance == "是":
                    relevant_papers.append((filename, title, reason))
                print("-------------------")
    return relevant_papers

# 主程式
if __name__ == "__main__":
    folder_path = "paper_folder"
    search_topic = "使用machine learning來做path loss prediction"
    csv_path = "paper_relevance.csv"
    
    print(f"搜索主題: {search_topic}")
    relevant_papers = process_pdf_folder(folder_path, search_topic, csv_path)
    
    print("\n相關論文:")
    for paper, title, reason in relevant_papers:
        print(f"文件: {paper}")
        print(f"標題: {title}")
        print(f"原因: {reason}")
        print("-------------------")
    
    print(f"\n所有論文的相關性分析已保存至 {csv_path}")