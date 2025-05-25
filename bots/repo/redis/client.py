import asyncio
from redis.asyncio import Redis
from config import Config

class RedisClient:
    _client = None
    _lock = asyncio.Lock()

    @classmethod
    async def get_client(cls) -> Redis:
        if cls._client is None or not await cls._check_connection():
            await cls._reconnect()
        return cls._client

    @classmethod
    async def _check_connection(cls) -> bool:
        try:
            return await cls._client.ping()
        except Exception:
            return False

    @classmethod
    async def _reconnect(cls):
        async with cls._lock:
            if cls._client:
                await cls._client.close()
            cls._client = Redis(
                host=Config.REDIS_HOST,
                port=Config.REDIS_PORT,
                db=Config.REDIS_DB,
                password=Config.REDIS_PASSWORD,
                ssl=Config.REDIS_SSL,
                decode_responses=True,
                socket_connect_timeout=5,
                retry_on_timeout=True
            )

    @classmethod
    async def close(cls):
        if cls._client:
            await cls._client.close()
            cls._client = None