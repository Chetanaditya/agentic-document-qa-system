from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from routes.auth import router as auth_router

# Routers
from routes.upload import router as upload_router
from routes.chat import router as chat_router
from routes.document_chat import router as document_chat_router



app = FastAPI(
    title="Agentic RAG Q&A System",
    description="Document-grounded AI Assistant using Ollama + ChromaDB",
    version="1.0.0"
)

# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict later in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Directories
# --------------------------------------------------

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

CHROMA_DIR = Path("chroma_db")
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Include Routers
# --------------------------------------------------

app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(document_chat_router)
app.include_router(auth_router)

# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/")
async def root():
    return {
        "status": "running",
        "project": "Agentic RAG Q&A System",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }


# --------------------------------------------------
# Startup Event
# --------------------------------------------------

@app.on_event("startup")
async def startup_event():
    print("\n" + "=" * 50)
    print(" Agentic RAG Backend Started ")
    print("=" * 50)
    print(f" Upload Directory : {UPLOAD_DIR}")
    print(f" Chroma Directory : {CHROMA_DIR}")
    print("=" * 50 + "\n")


# --------------------------------------------------
# Shutdown Event
# --------------------------------------------------

@app.on_event("shutdown")
async def shutdown_event():
    print("\nShutting down Agentic RAG Backend...\n")