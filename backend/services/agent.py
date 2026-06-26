from services.retriever import retrieve_chunks
from services.generator import generate
from services.query_rewriter import query_rewriter
from services.re_ranker import rerank_chunks
from services.reasoning_agent import reasoning_agent
from services.document_selector import select_documents
from services.vector_store import get_collection
from services.context_evaluator import context_evaluator

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


MAX_ITERATIONS = 2


def agentic_answer(
    query,
    retrieval_k=10,
    rerank_top_n=3
):

    print("\n========== AGENT START ==========")
    print("USER QUERY:", query)

    # ---------------------------------------------------
    # STEP 1 : QUERY REWRITER
    # ---------------------------------------------------

    rewritten_query = query_rewriter(query)

    print("REWRITTEN QUERY:", rewritten_query)

    # ---------------------------------------------------
    # STEP 2 : GET AVAILABLE DOCUMENTS
    # ---------------------------------------------------

    collection = get_collection()

    results = collection.get(include=["metadatas"])

    document_list = sorted(
        list(
            {
                metadata["source"]
                for metadata in results["metadatas"]
                if metadata and "source" in metadata
            }
        )
    )

    print("\n===== AVAILABLE DOCUMENTS =====")
    for doc in document_list:
        print("-", doc)

    # ---------------------------------------------------
    # STEP 3 : DOCUMENT SELECTION
    # ---------------------------------------------------

    selected_documents = select_documents(
        rewritten_query,
        document_list
    )

    print("\n===== SELECTED DOCUMENTS =====")
    print(selected_documents)

    if not selected_documents:
        print("No document selected.")
        selected_documents = document_list

    # ---------------------------------------------------
    # ITERATIVE RETRIEVAL
    # ---------------------------------------------------

    all_chunks = []

    for iteration in range(MAX_ITERATIONS):

        print(f"\n========== ITERATION {iteration + 1} ==========")

        new_chunks = retrieve_chunks(
            rewritten_query,
            top_k=retrieval_k,
            selected_documents=selected_documents
        )

        print("NEW CHUNKS:", len(new_chunks))

        all_chunks.extend(new_chunks)

        unique_chunks = []
        seen = set()

        for chunk in all_chunks:

            key = (
                chunk["text"],
                chunk.get("source")
            )

            if key not in seen:
                unique_chunks.append(chunk)
                seen.add(key)

        print("UNIQUE CHUNKS:", len(unique_chunks))

        chunks = rerank_chunks(
            rewritten_query,
            unique_chunks,
            top_n=rerank_top_n
        )

        decision = reasoning_agent(
            rewritten_query,
            chunks
        )

        print("DECISION:", decision["decision"])
        print("REASON:", decision["reason"])

        if decision["decision"] == "ENOUGH_CONTEXT":
            print("CONTEXT IS SUFFICIENT")
            break

        print("RETRIEVING AGAIN...")

    # ---------------------------------------------------
    # BUILD CONTEXT
    # ---------------------------------------------------

    context = "\n\n".join(
        chunk["text"]
        for chunk in chunks
    )

    print("\n===== FINAL CONTEXT =====")
    print(context[:1500])
    print("=========================\n")

    # ---------------------------------------------------
    # CONTEXT EVALUATION
    # ---------------------------------------------------

    evaluation = context_evaluator(
        rewritten_query,
        context
    )

    print("\n===== CONTEXT EVALUATION =====")
    print(evaluation)

    if evaluation["status"] == "INSUFFICIENT":

        print("Context is insufficient.")

        return {
            "answer": "I could not find sufficient information in the uploaded document.",
            "chunks": chunks,
            "citations": []
        }

    # ---------------------------------------------------
    # GENERATE ANSWER
    # ---------------------------------------------------

    prompt = DOCUMENT_PROMPT.format(
        context=context,
        query=query
    )

    answer = generate(prompt)

    citations = []
    seen = set()

    for chunk in chunks:

        source = chunk.get("source", "Unknown")

        if source not in selected_documents:
            continue

        if source in seen:
            continue

        citations.append(
            {
                "source": source,
                "page": chunk.get("page", "N/A"),
                "text": chunk.get("text", "")
            }
        )

        seen.add(source)

    print("\n========== AGENT END ==========\n")

    return {
        "answer": answer,
        "citations": citations,
        "chunks": chunks
    }