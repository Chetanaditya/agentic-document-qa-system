# 🚀 Agentic RAG Q&A System v1.0

A modular **Agentic Retrieval-Augmented Generation (RAG)** system built completely with **local LLMs** using **Ollama**, **Qwen 2.5**, **FastAPI**, **React**, **ChromaDB**, and **CrossEncoder Re-Ranking**.

Unlike traditional RAG pipelines, this project introduces multiple specialized AI agents responsible for query rewriting, document selection, reasoning, context evaluation, and grounded response generation.

The entire system runs locally without relying on external APIs.

---

# 🌟 Features

### 📄 Multi-format Document Ingestion

Supports uploading and indexing:

* PDF
* DOCX
* CSV
* TXT

Each uploaded document is:

* Parsed
* Chunked
* Embedded
* Stored inside ChromaDB

---

## 🧠 Agentic Retrieval Pipeline

Instead of a traditional Retrieve → Generate workflow, this project follows an **agent-based architecture**.

### 1. Query Rewriter Agent

Rewrites user queries into more retrieval-friendly semantic queries.

Example:

User:

> What are my programming skills?

↓

Rewritten Query:

> resume programming languages technical skills

---

### 2. Document Selection Agent

Selects the most relevant uploaded document(s) before retrieval.

This significantly reduces unnecessary retrieval from unrelated documents.

---

### 3. Semantic Retriever

Uses **MXBAI-Embed-Large** embeddings with **ChromaDB** vector search to retrieve semantically similar chunks.

---

### 4. CrossEncoder Re-Ranker

Retrieved chunks are re-ranked using

**cross-encoder/ms-marco-MiniLM-L-6-v2**

This improves retrieval precision by ranking chunks according to semantic relevance instead of embedding similarity alone.

---

### 5. Reasoning Agent

Acts as the decision-making component.

Responsible for determining whether:

* enough evidence has been retrieved
* another retrieval iteration is required

This forms the basis of iterative retrieval.

---

### 6. Context Evaluator

Evaluates the final retrieved context before answer generation.

Checks:

* Relevance
* Completeness
* Confidence

If insufficient evidence exists, the system avoids hallucinating.

---

### 7. Generator

Uses **Qwen 2.5 (Ollama)** to generate grounded responses using only the retrieved context.

The model is explicitly instructed to avoid hallucination and answer only from the provided documents.

---

# 🏗 Current Architecture

```text
User
 │
 ▼
React Frontend
 │
 ▼
FastAPI Backend
 │
 ▼
Query Rewriter Agent
 │
 ▼
Document Selection Agent
 │
 ▼
Semantic Retrieval
 │
 ▼
CrossEncoder Re-Ranker
 │
 ▼
Reasoning Agent
 │
 ▼
Context Evaluator
 │
 ▼
Grounded Response Generator
 │
 ▼
Frontend
```

---

# 🧩 Tech Stack

## Backend

* Python
* FastAPI
* Ollama
* Qwen 2.5
* ChromaDB
* Sentence Transformers
* CrossEncoder
* MXBAI-Embed-Large

## Frontend

* React.js
* JavaScript
* HTML
* CSS
* React Markdown

---

# 📂 Project Structure

```
backend/

services/

document_loader.py

chunker.py

embeddings.py

vector_store.py

query_rewriter.py

document_selector.py

retriever.py

re_ranker.py

reasoning_agent.py

context_evaluator.py

generator.py

agent.py

routes/

frontend/

React Application
```

---

# Retrieval Workflow

```
Upload Document

↓

Document Loader

↓

Chunking

↓

Embeddings

↓

ChromaDB

═══════════════════════

User Query

↓

Query Rewriter

↓

Document Selection

↓

Retriever

↓

CrossEncoder

↓

Reasoning Agent

↓

Context Evaluator

↓

Generator

↓

Final Response
```

---

# Current Capabilities

✅ Multi-document ingestion

✅ Semantic search

✅ CrossEncoder re-ranking

✅ Query rewriting

✅ Document selection

✅ Iterative retrieval framework

✅ Context evaluation

✅ Local LLM inference

✅ Grounded document Q&A

✅ Citation generation

✅ Modular architecture

---

# Challenges Faced During Development

## Retrieval Quality

Initially, retrieved chunks often contained irrelevant information.

### Solution

Introduced:

* Query Rewriter
* CrossEncoder Re-ranking

This significantly improved retrieval precision.

---

## Multi-document Retrieval

When multiple documents existed in ChromaDB, unrelated chunks were retrieved.

### Solution

Implemented a Document Selection Agent that routes retrieval toward the most relevant uploaded document(s).

---

## Hallucinations

The model occasionally generated information not present in uploaded documents.

### Solution

Designed a strict system prompt instructing the generator to answer only from retrieved context.

---

## Retrieval Validation

The system previously generated responses even when retrieval quality was poor.

### Solution

Added a dedicated Context Evaluator to verify the sufficiency of retrieved evidence before generation.

---

## Iterative Retrieval

Traditional RAG performs retrieval only once.

### Solution

Introduced a Reasoning Agent capable of deciding whether another retrieval iteration is required.

---

# Future Roadmap (V2)

Planned improvements include:

* Hybrid Search (Dense + BM25)
* Metadata-aware Retrieval
* Semantic Chunking
* Adaptive Chunk Sizes
* Conversation Memory
* User Authentication
* Multi-user Support
* Docker Deployment
* Redis Caching
* Streaming Responses
* Source Highlighting
* Confidence Scoring
* Performance Monitoring
* Production Logging

---

# Goals

This project aims to explore how modular AI agents can improve Retrieval-Augmented Generation by separating responsibilities across retrieval, reasoning, evaluation, and generation while keeping the entire system fully local and privacy-friendly.

---

# Acknowledgements

Built using:

* Ollama
* Qwen 2.5
* ChromaDB
* FastAPI
* React
* Sentence Transformers
* CrossEncoder (MS MARCO)
* MXBAI-Embed-Large

---

# License

This project is intended for educational, research, and portfolio purposes.
