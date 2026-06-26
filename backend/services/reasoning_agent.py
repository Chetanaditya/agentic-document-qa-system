import json
import logging
import ollama

logger = logging.getLogger(__name__)

MODEL_NAME = "qwen2.5:3b"


REASONING_PROMPT = """
You are the Reasoning Agent in an Agentic Retrieval-Augmented Generation (RAG) system.

You are NOT answering the user's question.

Your ONLY responsibility is to decide whether the currently retrieved context is sufficient.

User Query:
{query}

Retrieved Context:
{context}

Instructions:

1. If the retrieved context contains enough information to confidently answer the user's question,
return:

{{
    "decision": "ENOUGH_CONTEXT",
    "reason": "...",
    "new_query": null
}}

2. If important information is missing,
return:

{{
    "decision": "MORE_RETRIEVAL",
    "reason": "...",
    "new_query": "a better semantic search query"
}}

Rules:

- Never answer the user's question.
- Think like a retrieval planner.
- The new_query should be optimized for semantic retrieval.
- Return ONLY valid JSON.
"""


def reasoning_agent(query, chunks):

    if not chunks:

        return {
            "decision": "MORE_RETRIEVAL",
            "reason": "No chunks retrieved.",
            "new_query": query
        }

    context = "\n\n".join(
        chunk["text"] for chunk in chunks
    )

    prompt = REASONING_PROMPT.format(
        query=query,
        context=context[:4000]
    )

    try:

        response = ollama.generate(
            model=MODEL_NAME,
            prompt=prompt,
            options={
                "temperature": 0,
                "num_predict": 200
            }
        )

        raw = response["response"].strip()

        logger.info(raw)

        result = json.loads(raw)

        return {
            "decision": result.get(
                "decision",
                "ENOUGH_CONTEXT"
            ),
            "reason": result.get(
                "reason",
                ""
            ),
            "new_query": result.get(
                "new_query",
                None
            )
        }

    except Exception as e:

        logger.error(e)

        return {
            "decision": "ENOUGH_CONTEXT",
            "reason": "Reasoning failed.",
            "new_query": None
        }