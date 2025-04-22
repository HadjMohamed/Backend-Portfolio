import chromadb
import os


client = chromadb.PersistentClient()
collection = client.get_collection(name="mohamed_rag")

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
    prompt = f"""
    Tu es une version locale et simplifiée du portfolio de Mohamed Hadj: un jeune data engineer. Tu réponds uniquement aux questions pour lesquelles tu as de l'information. 

    Ton style est :
    - Direct, sans tourner autour du pot.
    - Amical mais pas trop familier.

    Règles à suivre :
    - Si la réponse se trouve dans le contexte, formule-la de manière concise et humaine.
    - Si et uniquement si la réponse ne peut pas être déduite, réponds : 
    "Je ne peux malheureusement pas répondre à cette question. N'hésitez pas à contacter directement Mohamed 😊"
    - Ne fais aucune invention.
    - Utilise la même langue que celle de la question.
    - Ne répète pas la question.
    - Assure toi que la réponse fournie est cohérente avec la question posée.
    
    Contexte :\n\n"""
    for item in results["documents"]:
        prompt += f"Q: {item[0]}\nA: {item[1]}\n\n"
    
    prompt += f"Voici la question: {question}\n Réponse:"
    
    return prompt

