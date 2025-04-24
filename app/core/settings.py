import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3:8b")
OPENROUTER_API_KEY = os.getenv("API_KEY")
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "mohamed_rag")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

FAQ_PATH = os.getenv("FAQ_PATH", "app/data/faq_mohamed_hadj.json")
RAG_THRESHOLD = float(os.getenv("RAG_THRESHOLD", 0.9))
