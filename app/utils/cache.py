import redis.asyncio as redis
import json
import logging

logger = logging.getLogger(__name__)

# Create a Redis client
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

async def get_cached_data(key: str):
    try:
        cached = await redis_client.get(key)
        if cached:
            return json.loads(cached)
    except Exception as e:
        logger.error("Redis get error: %s", e)
    return None

async def set_cached_data(key: str, value, expire_seconds: int = 6400):
    try:
        await redis_client.set(key, json.dumps(value), ex=expire_seconds)
    except Exception as e:
        logger.error("Redis set error: %s", e)
