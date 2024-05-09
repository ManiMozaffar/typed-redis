import json
from functools import lru_cache
from logging import getLogger
from typing import TypeVar

from pydantic import TypeAdapter
from redis.asyncio import ConnectionPool as AsyncConnectionPool
from redis.asyncio.client import Redis

from src.channels import RedisChannels

ChannelT = TypeVar("ChannelT", bound=RedisChannels)

logger = getLogger(__name__)


class RedisManager:
    def __init__(self, redis_connection_pool: AsyncConnectionPool):
        self.redis = Redis(connection_pool=redis_connection_pool)
        self.redis_connection_pool = redis_connection_pool

    async def publish(self, payload: RedisChannels):
        await self.redis.publish(payload.channel, payload.data.model_dump_json())

    async def disconnect(self):
        await self.redis_connection_pool.aclose()

    async def listen(self, channel_type: type[ChannelT]):
        pubsub = self.redis.pubsub()
        channel = channel_type.get_channel()
        await pubsub.subscribe(channel.value)
        logger.info(f"Subscribed to {channel}. Waiting for messages...")
        async for message in pubsub.listen():
            if message["type"] == "message":
                msg = message["data"].decode("utf-8")
                logger.debug(f"Received message: {msg}")
                yield TypeAdapter(channel_type).validate_python(
                    {"data": json.loads(msg), "channel": channel.value}
                )


@lru_cache
def get_redis():
    return RedisManager(
        redis_connection_pool=AsyncConnectionPool.from_url("redis://localhost")
    )
