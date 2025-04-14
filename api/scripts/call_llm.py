import os
from openai import OpenAI
from loguru import logger

def call_llm(prompt: str)-> str:
    """
    Call the OpenRouter API with the given prompt and return the response.
    """
    logger.info('Connecting to OpenRouter API...')
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("API_KEY"),
    )
    logger.success('Connected to OpenRouter API')
    logger.info('Passing prompt to Deepseek model...')
    completion = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[
            {
                "role": "user",
                "content": prompt
            },
        ]
    )
    
    return completion.choices[0].message.content # type: ignore