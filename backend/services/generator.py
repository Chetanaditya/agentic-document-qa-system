import ollama
import time

MODEL_NAME = "qwen2.5:3b"


def generate(prompt: str):
    try:
        print("\n" + "=" * 60)
        print("CALLING OLLAMA")
        print("=" * 60)

        start = time.time()

        response = ollama.generate(
            model=MODEL_NAME,
            prompt="/no_think\n" + prompt,
            options={
                "temperature": 1,
                "num_predict": 1000
            }
        )

        elapsed = time.time() - start

        print("OLLAMA RETURNED")
        print(f"OLLAMA TOOK: {elapsed:.2f} seconds")

        return response["response"]

    except Exception as e:
        print("\n" + "=" * 60)
        print("OLLAMA ERROR:")
        print(str(e))
        print("=" * 60)

        return f"Error generating response: {str(e)}"


def generate_answer(query: str, chunks: list):
    context = "\n\n".join(
        chunk["text"]
        for chunk in chunks
    )

    prompt = f"""
You are a document QA Assistant.

Use ONLY the context below.

Context:
{context}

Question:
{query}

Return ONLY the final answer.

Do NOT explain your reasoning.
Do NOT show thinking.
Do NOT show analysis.

Formatting Rules :

use proper markdown
do not place list on seperate lines 
do not generate empty lines between a list marker and it's content
use compact formatting
use bullet points for explanations
use numbered lists only when necessary
keep responses readable and concise

Answer:
"""

    print("\n===== RETRIEVED CONTEXT =====")
    print(context)
    print("=============================")

    return generate(prompt)