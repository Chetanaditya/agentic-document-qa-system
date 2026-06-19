from services.generator import generate


def decide_action(query: str, has_document: bool):

    if not has_document:
        return "GENERAL_CHAT"

    prompt = f"""
You are an AI Routing Agent for an Agentic RAG system.

Your task is to classify every user query into exactly one category:

DOCUMENT_SEARCH

or

GENERAL_CHAT

Classification Rules:

DOCUMENT_SEARCH:
Choose DOCUMENT_SEARCH if the query is likely asking for information that could exist inside an uploaded document.

Examples:

* Questions about a resume, CV, applicant, candidate, employee, policy, report, contract, invoice, article, PDF, research paper, or uploaded file.
* Questions asking for names, dates, skills, projects, qualifications, achievements, experience, education, certifications, or other document contents.
* Questions that refer to:

  * "the applicant"
  * "the employee"
  * "the candidate"
  * "the resume"
  * "the document"
  * "the report"
  * "the uploaded file"
* Requests to summarize, explain, extract, list, compare, or analyze document contents.
* Single-word queries that could refer to a document section:

  * PROJECTS
  * SKILLS
  * EDUCATION
  * EXPERIENCE
  * CERTIFICATIONS
  * ACHIEVEMENTS
* Any query that can reasonably be answered using information from an uploaded document.

GENERAL_CHAT:
Choose GENERAL_CHAT only if the query clearly does not require document information.

Examples:

* Tell me a joke.
* What is Python?
* Explain machine learning.
* Write a Java program.
* What is the capital of France?
* How do I prepare for an interview?
* Casual conversation or greetings.

Important Decision Rule:

If you are uncertain, choose DOCUMENT_SEARCH.

When a document is available, prefer DOCUMENT_SEARCH unless the query is clearly general conversation or general knowledge.

User Query:
{query}

Respond with ONLY one label:

DOCUMENT_SEARCH

or

GENERAL_CHAT

"""

    decision = generate(prompt).strip()

    print("PLANNER DECISION:", decision)

    if "DOCUMENT_SEARCH" in decision:
        return "DOCUMENT_SEARCH"
    return "GENERAL_CHAT"