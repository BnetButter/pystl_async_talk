import asyncio

loop = asyncio.get_event_loop()
queue = asyncio.Queue()


async def producer():
    i = 0
    while True:
        await queue.put(i)
        await asyncio.sleep(1)
        i += 1

async def consumer():
    while True:
        result = await queue.get()
        yield result

async def async_for():
    async for message in consumer():
        print(message)


loop.create_task(producer())
loop.create_task(async_for())
loop.run_forever()