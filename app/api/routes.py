from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag_logic import generate_response

router = APIRouter()

class Question(BaseModel):
    """
    Model for the question input.
    """
    question: str

    
@router.post('/ask')
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

@router.get('/health')
async def health():
    """
    Health check endpoint.
    """
    return {"status": "ok"}