from services.retriever import retrieve_chunks
from services.generator import generate
from services.query_rewriter import query_rewriter
from services.re_ranker import rerank_chunks


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
    """
    Temporary Context Evaluator.

    For now, if retrieval + reranking
    returns at least one chunk, we consider
    the context sufficient.

    Later this will become an LLM-based
    Context Evaluation Agent.
    """

    return len(chunks) > 0


def agentic_answer(
    query,
    retrieval_k=10,
    rerank_top_n=3
):

    print("\n========== AGENT START ==========")
    print("USER QUERY:", query)

    # STEP 1 : QUERY REWRITING

    rewritten_query = query_rewriter(query)

    print("REWRITTEN QUERY:", rewritten_query)

    # STEP 2 : RETRIEVAL

    chunks = retrieve_chunks(
        rewritten_query,
        top_k=retrieval_k
    )

    print("RETRIEVED CHUNKS:", len(chunks))

    # STEP 3 : RE-RANKING

    chunks = rerank_chunks(
        rewritten_query,
        chunks,
        top_n=rerank_top_n
    )

    # STEP 4 : CONTEXT EVALUATION

    sufficient = context_is_sufficient(chunks)

    print("CONTEXT SUFFICIENT:", sufficient)

    if not sufficient:

        print("SWITCHING TO GENERAL CHAT")

        from services.general_chat import general_chat

        answer = general_chat(query)

        print("========== AGENT END ==========\n")

        return {
            "answer": answer,
            "chunks": [],
            "citations": []
        }

    # STEP 5 : BUILD CONTEXT

    context = "\n\n".join(
        chunk["text"]
        for chunk in chunks
    )

    print("\n===== FINAL CONTEXT =====")
    print(context[:1500])
    print("\n=========================")

    # STEP 6 : PROMPT CONSTRUCTION

    prompt = DOCUMENT_PROMPT.format(
        context=context,
        query=query
    )

    # STEP 7 : GENERATION

    answer = generate(prompt)

    # STEP 8 : BUILD CITATIONS

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