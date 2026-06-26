import json
import re

from services.generator import generate


SYSTEM_PROMPT = """
You are a Context Evaluation Agent.

Your job is to determine whether the retrieved context is sufficient to answer the user's question.

Evaluate the context based on:

1. Relevance
2. Completeness
3. Accuracy
4. Missing information

Return ONLY valid JSON.

Example:

{
    "status":"SUFFICIENT",
    "confidence":0.95,
    "reason":"The retrieved context fully answers the user's question."
}

Possible status values:

SUFFICIENT
PARTIAL
INSUFFICIENT
"""


def context_evaluator(query, context):

    prompt = f"""
{SYSTEM_PROMPT}

User Question:
{query}

Retrieved Context:
{context}
"""

    answer = generate(prompt)

    print("\n===== CONTEXT EVALUATOR =====")
    print(answer)

    try:

        match = re.search(r"\{.*\}", answer, re.DOTALL)

        if match:
            return json.loads(match.group())

    except Exception:
        pass

    return {
        "status": "PARTIAL",
        "confidence": 0.5,
        "reason": "Unable to evaluate context."
    }