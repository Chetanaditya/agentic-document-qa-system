import json
import ollama

MODEL_NAME = "qwen2.5:3b"


SYSTEM_PROMPT ="""
You are a Document Selection Agent.

Your ONLY job is to determine which uploaded document(s)
should be searched.

IMPORTANT RULES

1. You MUST choose ONLY from the document names provided.
2. Copy the filenames EXACTLY.
3. Never shorten or rename filenames.
4. If ONE document is enough, return ONLY that document.
5. Return multiple documents ONLY if the user's question truly requires information from multiple documents.
6. Return an empty list ONLY if none of the uploaded documents are relevant.
7. Output ONLY valid JSON.

Example:

Available Documents:
- Resume.docx
- LeavePolicy.pdf

User:
What is the applicant's name?

Output:

{
  "documents":[
      "Resume.docx"
  ]
}
"""


def select_documents(query: str, document_list: list[str]) -> list[str]:
    """
    Uses Qwen to determine which document(s)
    should be searched.
    """

    prompt = f"""
Available Documents:

{chr(10).join("- " + d for d in document_list)}

User Query:
{query}
"""

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            options={
                "temperature": 0
            }
        )

        answer = response["message"]["content"].strip()

        print("\n===== DOCUMENT SELECTOR =====")
        print(answer)
        print("=============================\n")

        parsed = json.loads(answer)

        documents = parsed.get("documents", [])

        valid_docs = [
            doc
            for doc in documents
            if doc in document_list
        ]

        return valid_docs

    except Exception as e:
        print("DOCUMENT SELECTOR ERROR:", e)

        # fallback
        return document_list