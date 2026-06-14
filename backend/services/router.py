import ollama

MODEL_NAME = "qwen2.5:3b"

def route_query(query: str):

    prompt = f"""
You are a routing agent.

Determine whether the user query requires
information from an uploaded document

Respond with ONLY one word:

Document
or
General

Query:
{query}
"""
    
    response = ollama.generate(
        model=MODEL_NAME,
        prompt=prompt,
        options={
            "temperature": 1
        }
    )

    decision = response["response"].strip().upper()

    print("\nROUTER DECISION : ")
    print(decision)

    print("\nQwery : ")
    print(query)

    return decision