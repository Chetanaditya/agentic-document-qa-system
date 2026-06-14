import ollama
import time

MODEL_NAME = "qwen2.5:3b"


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

Answer:
"""

    print("\n" + "=" * 60)
    print("QUERY:")
    print(query)
    print("=" * 60)

    print("CONTEXT LENGTH:", len(context))
    print("PROMPT LENGTH:", len(prompt))

    try:

        print("CALLING OLLAMA...")

        start = time.time()

        response = ollama.generate(
            model=MODEL_NAME,
            prompt="/no_think\n" + prompt,
            options={
                "temperature": 0,
                "num_predict": 1000
            }
        )

        elapsed = time.time() - start

        print("OLLAMA RETURNED")
        print(f"OLLAMA TOOK: {elapsed:.2f} seconds")

        print("\nMODEL RESPONSE TYPE:")
        print(type(response))

        print("\nMODEL RESPONSE:")
        print(response)

        print("=" * 60)

        answer = response["response"]

        return answer

    except Exception as e:

        print("\n" + "=" * 60)
        print("OLLAMA ERROR:")
        print(str(e))
        print("=" * 60)

        return f"Error generating response: {str(e)}"