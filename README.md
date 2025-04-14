# Mohamed RAG API

This project exposes a FastAPI-based REST API deployed on **Google Cloud Run**. It allows users to ask questions to a personalized assistant named **Mohamed**, powered by a combination of **Retrieval-Augmented Generation (RAG)** and a **Large Language Model (LLM)** to provide accurate, contextual answers.

---

## 📚 Features

- 🔍 **Document retrieval** using **ChromaDB** (vector database)
- 🧠 **RAG logic** to answer using relevant retrieved documents
- 🗣️ **Fallback to prompt-only mode** using a pre-defined FAQ if no relevant documents are found
- 🤖 **LLM integration** (DeepSeek V3 0324) for human-like response generation
- 🌐 Exposed as a **REST API** using FastAPI
- 🐳 Docker + Makefile setup for local runs and cloud deployment
- 🔧 Environment variables handled via `.env` file

---

## ⚙️ Architecture

```mermaid
flowchart TD
    Q[User Question] --> RAG{Is RAG relevant?}
    RAG -- Yes --> PromptRAG[→ Build context-based prompt from documents]
    RAG -- No --> PromptOnly[→ Build generic prompt from local JSON FAQ]
    PromptRAG & PromptOnly --> LLM[Call the LLM]
    LLM --> Response
