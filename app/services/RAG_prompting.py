import chromadb
import os
from app.core.settings import CHROMA_COLLECTION_NAME


client = chromadb.PersistentClient(path="chroma")
collection = client.get_collection(name=CHROMA_COLLECTION_NAME)

def collection_query(question :str)-> dict:
    """
    Query the ChromaDB collection for relevant documents.
    Args:
        question (str): The question to ask.
    Returns:
        tuple: A tuple containing the results and context.
    """
    results = collection.query(query_texts=[question], n_results=3)
    return results # type: ignore

def prompt_RAG(question: str, results: dict) -> str:
    """
    Generate a prompt for the RAG model if the answer is relevant.
    Args:
        question (str): The question to ask.
        results (dict): The results from the collection query.
        context (str): The context from the collection query.
    Returns:
        str: The generated prompt.
    """
    prompt = """Contexte :\n\n"""
    for item in results["documents"]:
        prompt += f"Q: {item[0]}\nA: {item[1]}\n\n"
    
    prompt += f"Voici la question: {question}\n Réponse:"
    
    return prompt

