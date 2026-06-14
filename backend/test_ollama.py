import ollama 

response = ollama.generate(
    model="qwen2.5:3b",
    prompt="What is 2+2?"
)

print(response)