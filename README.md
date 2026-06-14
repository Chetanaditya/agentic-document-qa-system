# 🤖 Agentic Document Q&A System

An AI-powered Document Question Answering System that enables users to upload documents and interact with them using natural language. The system leverages an Agentic Retrieval-Augmented Generation (Agentic RAG) architecture to retrieve relevant context, reason over retrieved information, and generate accurate, context-aware responses.

---

## 📌 Project Overview

Traditional document search systems rely on keyword matching and often struggle with understanding user intent. This project implements an Agentic RAG workflow that intelligently retrieves, analyzes, and generates responses from uploaded documents.

Users can upload documents and ask questions in natural language. The system retrieves relevant document chunks through semantic search and uses a Large Language Model (LLM) to generate grounded responses based on the retrieved content.

---

## 🚀 Features

- 📄 Document Upload and Processing
- ✂️ Intelligent Document Chunking
- 🔍 Semantic Search using Vector Embeddings
- 🗄️ ChromaDB Vector Database Integration
- 🤖 Agentic Retrieval-Augmented Generation (Agentic RAG)
- 💬 Conversational Question Answering
- 🧠 Context-Aware Response Generation
- 🌐 Full-Stack Application (React + FastAPI)
- ⚡ Local LLM Integration using Ollama
- 📚 Source-Grounded Responses

---

## 🏗️ System Architecture

```text
User Query
     │
     ▼
Question Router
     │
     ▼
Retriever Agent
     │
     ▼
ChromaDB Vector Store
     │
     ▼
Relevant Document Chunks
     │
     ▼
Response Generator (LLM)
     │
     ▼
Final Answer
```

---

## 🧠 Agentic RAG Workflow

1. User uploads a document.
2. Document is parsed and chunked.
3. Chunks are converted into vector embeddings.
4. Embeddings are stored in ChromaDB.
5. User submits a question.
6. Retrieval Agent identifies relevant document chunks.
7. Retrieved context is passed to the LLM.
8. LLM generates a grounded response.
9. Response is returned to the user.

---

## 🔄 Normal RAG vs Agentic RAG

| Normal RAG | Agentic RAG |
|------------|-------------|
| Simple retrieval followed by generation | Uses intelligent agents to decide retrieval and reasoning steps |
| Fixed workflow | Dynamic decision-making workflow |
| Limited reasoning capability | Enhanced reasoning and context selection |
| Basic document retrieval | Intelligent retrieval and response generation |
| Less adaptable | More flexible and scalable |

This project follows an **Agentic RAG architecture**, allowing the system to perform smarter retrieval and response generation compared to traditional RAG pipelines.

---

## 🛠️ Tech Stack

### Frontend
- React.js
- Vite
- CSS

### Backend
- FastAPI
- Python

### AI & Machine Learning
- Ollama
- Large Language Models (LLMs)
- Semantic Search
- Retrieval-Augmented Generation (RAG)

### Vector Database
- ChromaDB

### Version Control
- Git
- GitHub

---

## 📂 Project Structure

```text
agentic-document-qa-system
│
├── backend
│   ├── routes
│   │   ├── chat.py
│   │   ├── document_chat.py
│   │   └── upload.py
│   │
│   ├── services
│   │   ├── chunker.py
│   │   ├── document_loader.py
│   │   ├── embeddings.py
│   │   ├── generator.py
│   │   ├── ingestion.py
│   │   ├── retriever.py
│   │   ├── router.py
│   │   └── vector_store.py
│   │
│   └── main.py
│
├── chatbot
│   ├── src
│   ├── public
│   └── package.json
│
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/agentic-document-qa-system.git
```

### Backend Setup

```bash
cd backend

pip install -r requirements.txt

uvicorn main:app --reload
```

### Frontend Setup

```bash
cd chatbot

npm install

npm run dev
```

---

## 📖 Usage

1. Start the FastAPI backend.
2. Start the React frontend.
3. Upload a document.
4. Ask questions related to the uploaded document.
5. Receive context-aware responses generated from retrieved document content.

---

## 🎯 Learning Outcomes

Through this project, the following concepts were implemented and explored:

- Agentic AI Systems
- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Vector Databases
- Embedding Models
- Document Intelligence Systems
- FastAPI Development
- React Frontend Development
- Full-Stack AI Application Development
- LLM Integration

---

## 💼 Industry-Relevant Skills

- Artificial Intelligence
- Machine Learning
- Agentic AI
- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Vector Databases
- ChromaDB
- FastAPI
- Python Development
- React.js
- API Development
- Prompt Engineering
- LLM Applications
- Full-Stack Development
- Git & GitHub

---

## 🔮 Future Enhancements

- Multi-document querying
- PDF, DOCX, and TXT support
- Citation-based responses
- Hybrid Search (Keyword + Semantic)
- Memory-enabled conversations
- Multi-agent orchestration
- Cloud deployment

---

## 👨‍💻 Author

**Chetanaditya Neelam**

Engineering Student | AI/ML Enthusiast | Full-Stack AI Developer

Connect with me on LinkedIn and GitHub to explore more AI and Machine Learning projects.
