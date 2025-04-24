import os
import redis
import hashlib
from openai import OpenAI
from loguru import logger
from app.core.prompts import SYSTEM_PROMPT
from app.core.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, OPENROUTER_API_KEY

# Redis client In comment for deployment
# redis_client = redis.Redis(
#     host=REDIS_HOST,
#     port=REDIS_PORT,
#     password=REDIS_PASSWORD,
#     db=0,
#     decode_responses=True
# )

def call_llm(prompt: str) -> str:
    """
    Envoie le prompt au modèle DeepSeek (via OpenRouter) et renvoie la réponse. Utilise Redis pour le caching.
    """
    # cache_key = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    # cached = redis_client.get(cache_key)
    # if cached:
    #     logger.info("✅ Réponse depuis Redis")
    #     return str(cached)

    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )

        response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content
        if answer:
            #redis_client.set(cache_key, answer)
            logger.success("✅ Réponse générée et mise en cache")
            return answer

        logger.warning("🟡 Modèle n'a pas retourné de contenu")
        return "Je suis désolé, je n’ai pas pu formuler de réponse."

    except Exception as e:
        logger.error(f"❌ Erreur LLM : {e}")
        return "Désolé, une erreur est survenue lors de la génération de la réponse."
