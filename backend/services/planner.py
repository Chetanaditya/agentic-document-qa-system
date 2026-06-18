from services.generator import generate


def decide_action(query: str, has_document: bool):

    if not has_document:
        return "GENERAL_CHAT"

    prompt = f"""
You are an AI routing agent.

Your task is to classify the query into one category.

Categories:

DOCUMENT_SEARCH
- Questions about uploaded files
- Questions that appear to require information from a document
- Questions referring to an applicant, employee, report, resume, policy, contract, invoice, article, PDF or uploaded content

GENERAL_CHAT
- Jokes
- General knowledge
- Programming help
- Casual conversation
- Questions that do not require uploaded documents

User Query:
{query}

Respond with ONLY one word:

DOCUMENT_SEARCH
or
GENERAL_CHAT
"""

    decision = generate(prompt).strip()

    print("PLANNER DECISION:", decision)

    if "DOCUMENT_SEARCH" in decision:
        return "DOCUMENT_SEARCH"

    return "GENERAL_CHAT"