from services.generator import generate


def query_rewriter(query: str):

    prompt = f"""
You are a retrieval query rewriting agent.

Your job is to convert user questions into optimized search queries for a vector database.

Rules:
- Preserve the original meaning.
- Focus on important entities, concepts, section names, and keywords.
- Remove filler words.
- Keep the rewritten query short.
- Return ONLY the rewritten query.
- Do not explain anything.

User Question:
{query}

Rewritten Query:
"""

    rewritten_query = generate(prompt).strip()

    print("REWRITTEN QUERY:", rewritten_query)

    return rewritten_query