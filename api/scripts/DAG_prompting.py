import chromadb
from openai import OpenAI
import os

def collection_query(question :str)-> dict:
    """
    Query the ChromaDB collection for relevant documents.
    Args:
        question (str): The question to ask.
    Returns:
        tuple: A tuple containing the results and context.
    """
    client = chromadb.PersistentClient()
    collection = client.get_collection(name="mohamed_rag")
    # Perform a query on the collection
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
    prompt = f"""
    Tu es un assistant intelligent. Tu dois répondre à la question suivante uniquement à partir des informations fournies dans les documents ci-dessous.  
    - Si l'information est présente, réponds de manière claire et concise comme si tu étais Mohamed Hadj.  
    - Si elle ne l'est pas, dis simplement : "Je ne peux pas répondre à votre question sans prendre de risque. N'hésitez pas à contacter directement Mohamed Hadj :)"  
    - Ne fais pas d'invention ni de supposition.  
    - Ne répète pas la question.  
    - Ta réponse doit être directe, sans contexte ou explication superflue.
    - Réponds dans la langue dans laquelle la question est posée.
    
    Voici des informations sur Mohamed Hadj :\n\n"""
    for item in results["documents"]:
        prompt += f"Q: {item[0]}\nA: {item[1]}\n\n"
    
    prompt += f"Voici la question: {question}\n Réponse:"
    
    return prompt


if __name__ == "__main__":
    question = "Qui est Mohamed Hadj ?"
    results = collection_query(question)
    print("Results:", results)

