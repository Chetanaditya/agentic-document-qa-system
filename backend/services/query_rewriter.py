from services.generator import generate


def decide_action(query: str):
    prompt = f"""
You are a planning agent.

User Query:
{query}

Decide:

1. DOCUMENT_SEARCH
2. GENERAL_CHAT

Respond with only one word.
"""

    response = generate(prompt)

    if "DOCUMENT_SEARCH" in response:
        return "DOCUMENT_SEARCH"

    return "GENERAL_CHAT"