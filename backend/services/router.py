import ollama
import re
import logging

logger = logging.getLogger(__name__)

MODEL_NAME = "qwen2.5:3b"

ROUTER_PROMPT_TEMPLATE = """
You are a query routing classifier for a RAG system.

Document Available: {document_status}

Your task is to classify the user's query into exactly one category:

DOCUMENT
GENERAL

DOCUMENT:
- Questions about uploaded documents
- Questions about resumes, reports, PDFs, policies, invoices, research papers, contracts
- Questions about applicants, employees, candidates, projects, skills, education, achievements, certifications, publications
- Short section queries:
  projects
  skills
  education
  experience
  certifications
  achievements
  publications
- Ambiguous queries that could reasonably be answered from a document

GENERAL:
- Jokes
- Casual conversation
- General knowledge
- Programming help unrelated to document contents
- Questions clearly unrelated to any uploaded document

Important Rules:

1. If a document is available and the query is ambiguous, choose DOCUMENT.
2. If the query could plausibly be answered using the uploaded document, choose DOCUMENT.
3. Only choose GENERAL when the query is clearly unrelated to the document.
4. Respond with EXACTLY ONE WORD.


User Query:
{query}

Answer:
"""


def route_query(query: str, has_document: bool):

    default = "DOCUMENT" if has_document else "GENERAL"

    document_status = (
        "YES"
        if has_document
        else "NO"
    )

    prompt = ROUTER_PROMPT_TEMPLATE.format(
        query=query.strip(),
        document_status=document_status
    )

    try:

        response = ollama.generate(
            model=MODEL_NAME,
            prompt=prompt,
            options={
                "temperature": 0,
                "num_predict": 5,
                "stop": ["\n"]
            }
        )

    except Exception as e:

        logger.error(
            f"Router model call failed: {e}"
        )

        return default

    raw_output = (
        response
        .get("response", "")
        .strip()
        .upper()
    )

    decision = _parse_decision(
        raw_output,
        default
    )

    logger.info(
        f"QUERY: {query} | "
        f"DOC: {has_document} | "
        f"RAW: {raw_output} | "
        f"DECISION: {decision}"
    )

    return decision


def _parse_decision(
    raw_output: str,
    default: str
):

    if (
        "DOCUMENT" in raw_output
        and "GENERAL" not in raw_output
    ):
        return "DOCUMENT"

    if (
        "GENERAL" in raw_output
        and "DOCUMENT" not in raw_output
    ):
        return "GENERAL"

    match = re.search(
        r"\b(DOCUMENT|GENERAL)\b",
        raw_output
    )

    if match:
        return match.group(1)

    logger.warning(
        f"Unparseable router output: "
        f"{raw_output!r}. "
        f"Defaulting to {default}"
    )

    return default