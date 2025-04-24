import json
from openai import OpenAI
import os


def prompt_only(question: str,data: list) -> str:
    """
    To complete the prompt with json data.
    Args:
        question (str): The question to ask.
    Returns:
        str: The answer from the model.
    """
    prompt = """Contexte :\n\n"""
    for item in data:
        prompt += f"Q: {item['question']}\nA: {item['reponse']}\n\n"

    # Ajouter la question utilisateur
    prompt += f"Voici la question: {question}\nRéponse:"
    
    return prompt


