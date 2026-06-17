from services.generator import generate


def context_is_sufficient(query, context):

    prompt = f"""
Question:
{query}

Retrieved Context:
{context}

Can this context answer the question?

Reply only:

YES
or
NO
"""

    response = generate(prompt)

    return "YES" in response.upper()