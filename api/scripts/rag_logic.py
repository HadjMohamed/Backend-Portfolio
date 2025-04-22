"""
Define the RAG logic: if the answer is relevant (score<1), use the RAG model; otherwise, use the prompt-only model.
"""

from scripts.RAG_prompting import collection_query, prompt_RAG
from scripts.prompt_only_qa import prompt_only
from scripts.call_llm import call_llm
import json
from loguru import logger

RAG_THRESHOLD = 0.9

JSON_PATH = "faq_mohamed_hadj.json"

def generate_response(question: str) -> str:
    results = collection_query(question)
    filtered_results = [
    {"document": document, "distance": distance}
    for document, distance in zip(results["documents"], results["distances"][0])
    if distance < RAG_THRESHOLD
    ]
    
    if filtered_results:
        logger.info(f"RAG succeded with {len(filtered_results)} results, passing it to the LLM...")
        prompt = prompt_RAG(question,results)
    else:
        logger.info("RAG not relevant enough, using prompt-only model...")
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        prompt = prompt_only(question, data)

    return call_llm(prompt)


    