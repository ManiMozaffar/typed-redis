# a software with sub program


from src.channels import FooChannel
from src.manager import get_redis
from src.models import FooData


async def fn():
    redis_manager = get_redis()
    await redis_manager.publish(FooChannel(data=FooData(test="something")))
    await redis_manager.disconnect()


if __name__ == "__main__":
    import asyncio

    asyncio.run(fn())
