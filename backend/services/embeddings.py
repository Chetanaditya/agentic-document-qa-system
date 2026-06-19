import ollama


EMBED_MODEL = "mxbai-embed-large:335m "


def get_embedding(text: str):

    response = ollama.embeddings(
        model=EMBED_MODEL,
        prompt=text
    )

    return response["embedding"]