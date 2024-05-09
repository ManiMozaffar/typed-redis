# a software with sub program


import asyncio

from aioclock import AioClock, Depends, Forever, OnShutDown

from src.channels import FooChannel
from src.manager import RedisManager, get_redis

app = AioClock()


@app.task(trigger=Forever())
async def sub(redis_manager: RedisManager = Depends(get_redis)):
    async for message in redis_manager.listen(FooChannel):
        print("Received foo message")
        print(message)


@app.task(trigger=OnShutDown())
async def shutdown(redis_manager: RedisManager = Depends(get_redis)):
    await redis_manager.disconnect()


if __name__ == "__main__":
    asyncio.run(app.serve())
