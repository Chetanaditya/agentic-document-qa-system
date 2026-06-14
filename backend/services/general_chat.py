import ollama

MODEL_NAME = "qwen2.5:3b"

def general_chat(qwery: str):
    response = ollama.generate(
        model=MODEL_NAME,
        prompt=qwery
    )

    return response["response"]