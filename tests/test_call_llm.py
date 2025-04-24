import time
import hashlib
import redis
from services.rag_logic import generate_response
from core.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD


redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=0,
    decode_responses=True
)

def test_llm_response_simple():
    question = "Quels langages utilise Mohamed ?"
    start = time.time()
    response = generate_response(question)
    duration = time.time() - start

    print(f"\n⏱ Réponse en {duration:.2f} sec :\n{response}\n")

    assert isinstance(response, str)
    assert len(response) > 0
    assert "Python" in response or "data" in response.lower()

def test_cache_efficiency():
    question = "Quels outils maîtrise Mohamed ?"
    cache_key = hashlib.sha256(question.encode("utf-8")).hexdigest()

    # Première requête (non en cache)
    redis_client.delete(cache_key)
    uncached_response = generate_response(question)

    # Deuxième requête (en cache)
    start = time.time()
    cached_response = generate_response(question)
    duration = time.time() - start

    print(f"\n⚡ Réponse depuis cache : {duration:.2f} sec")

    assert uncached_response == cached_response
    assert duration < 1.0  # cache = très rapide

def test_llm_fallback():
    # Pose une question hors RAG pour forcer le fallback
    question = "Quelle est la circonférence de bras de Mohamed ?" 
    response = generate_response(question)

    assert "Je ne peux malheureusement pas répondre" in response or "désolé" in response.lower()
