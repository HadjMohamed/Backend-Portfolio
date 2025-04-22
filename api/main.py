from fastapi import FastAPI, HTTPException,Request
from pydantic import BaseModel
from contextlib import asynccontextmanager
from scripts.rag_logic import generate_response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hadjmohamed.github.io"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    """
    Model for the question input.
    """
    question: str

    
@app.post('/ask')
async def ask(data: Question):
    """
    Endpoint to ask a question to the model.
    """
    question = data.question
    
    if not question:
        raise HTTPException(status_code=400, detail="No question provided")
    
    # Ask the model
    answer = generate_response(question)
    
    return {"answer": answer}

@app.get('/health')
async def health():
    """
    Health check endpoint.
    """
    return {"status": "ok"}
