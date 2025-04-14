
import json
from openai import OpenAI
import os


def prompt_only(question: str,data: list) -> str:
    """
    Ask a question to deepseek model by passing the json data.
    Args:
        question (str): The question to ask.
    Returns:
        str: The answer from the model.
    """
    prompt = """
    Tu es un assistant intelligent. Tu dois répondre à la question suivante uniquement à partir des informations fournies dans les documents ci-dessous.  
    - Si l'information est présente, réponds de manière claire et concise.  
    - Si elle ne l'est pas, dis simplement : "Je ne peux pas répondre à votre question sans prendre de risque. N'hésitez pas à contacter directement Mohamed Hadj :)"  
    - Ne fais pas d'invention ni de supposition.  
    - Ne répète pas la question.  
    - Ta réponse doit être directe, sans contexte ou explication superflue.
    - Réponds dans la langue dans laquelle la question est posée.
    
    Voici des informations sur Mohamed Hadj :\n\n"""
    for item in data:
        prompt += f"Q: {item['question']}\nA: {item['reponse']}\n\n"

    # Ajouter la question utilisateur
    prompt += f"Question: {question}\nRéponse:"
    
    return prompt


