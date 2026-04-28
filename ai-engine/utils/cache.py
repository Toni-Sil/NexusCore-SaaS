import redis.asyncio as aioredis
import json
import os


class CacheService:
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self._client = None

    async def _get_client(self):
        if not self._client:
            self._client = aioredis.from_url(self.redis_url)
        return self._client

    async def get(self, key: str):
        client = await self._get_client()
        value = await client.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(self, key: str, value: dict, ttl: int = 3600):
        client = await self._get_client()
        await client.setex(key, ttl, json.dumps(value))
