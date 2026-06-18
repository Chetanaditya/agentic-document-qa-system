from services.retriever import retrieve_chunks
from services.generator import generate
from services.planner import decide_action
from services.query_rewriter import query_rewriter


DOCUMENT_PROMPT = """
You are an intelligent document analysis assistant.

Answer ONLY using the retrieved document context.

Rules:
- Use only information found in the context.
- Write professionally and clearly.
- If the answer exists in the context, answer confidently.
- If the answer is not present in the context, clearly state:
  "I could not find this information in the uploaded document."
- Do not hallucinate.
- Do not make assumptions.

Context:
{context}

Question:
{query}

Answer:
"""


def context_is_sufficient(chunks):
    return len(chunks) > 0


def agentic_answer(query, top_k=3):

    print("\n========== AGENT START ==========")
    print("USER QUERY:", query)

    # Planner
    action = decide_action(
        query=query,
        has_document=True
    )

    print("PLANNER:", action)

    # GENERAL CHAT ROUTE
    if action == "GENERAL_CHAT":

        from services.general_chat import general_chat

        answer = general_chat(query)

        print("========== AGENT END ==========\n")

        return {
            "answer": answer,
            "chunks": [],
            "citations": []
        }

    # DOCUMENT ROUTE

    rewritten_query = query_rewriter(query)

    print("REWRITTEN QUERY:", rewritten_query)

    chunks = retrieve_chunks(
        rewritten_query,
        top_k
    )

    print("RETRIEVED CHUNKS:", len(chunks))

    sufficient = context_is_sufficient(chunks)

    print("CONTEXT SUFFICIENT:", sufficient)

    if not sufficient:

        return {
            "answer": "I could not find relevant information in the uploaded document.",
            "chunks": [],
            "citations": []
        }

    context = "\n\n".join(
        chunk["text"]
        for chunk in chunks
    )

    print("\n===== RETRIEVED CONTEXT =====")
    print(context[:1000])
    print("=============================\n")

    prompt = DOCUMENT_PROMPT.format(
        context=context,
        query=query
    )

    answer = generate(prompt)

    citations = []

    for chunk in chunks:

        citations.append({
            "source": chunk.get("source", "Unknown"),
            "page": chunk.get("page", "N/A"),
            "text": chunk.get("text", "")
        })

    print("========== AGENT END ==========\n")

    return {
        "answer": answer,
        "chunks": chunks,
        "citations": citations
    }