import ollama

#note: 要先執行ollama serve
model_name="llama3.1:8b"
question="where is Taiwan?"

response=ollama.chat(model=model_name, messages=[{"role":"user", "content": question},])

ollama_response=response["message"]["content"]
print(ollama_response)