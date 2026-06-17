from services.retriever import retrieve_chunks
from services.generator import generate


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


def rewrite_query(query):
    """
    Query rewriting placeholder.
    Can be upgraded later.
    """
    return query


def context_is_sufficient(chunks):
    """
    Simple evaluator.
    """
    return len(chunks) > 0


def agentic_answer(query, top_k=3):

    print("\n========== AGENT START ==========")
    print("USER QUERY:", query)

    # Step 1: Query Rewriter
    rewritten_query = rewrite_query(query)
    print("REWRITTEN QUERY:", rewritten_query)

    # Step 2: Retrieval
    chunks = retrieve_chunks(
        rewritten_query,
        top_k
    )

    print("RETRIEVED CHUNKS:", len(chunks))

    # Step 3: Evaluator
    sufficient = context_is_sufficient(chunks)
    print("CONTEXT SUFFICIENT:", sufficient)

    if not sufficient:

        return {
            "answer": "I could not find relevant information in the uploaded document.",
            "chunks": [],
            "citations": []
        }

    # Step 4: Build Context
    context = "\n\n".join(
        chunk["text"]
        for chunk in chunks
    )

    print("\n===== RETRIEVED CONTEXT =====")
    print(context[:1000])  # first 1000 chars
    print("=============================\n")

    # Step 5: Prompt Construction
    prompt = DOCUMENT_PROMPT.format(
        context=context,
        query=query
    )

    # Step 6: Generation
    answer = generate(prompt)

    # Step 7: Citations
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