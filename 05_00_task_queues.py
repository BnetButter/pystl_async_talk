import asyncio

loop = asyncio.get_event_loop()
queue = asyncio.Queue()

async def produce_num():
    i = 0
    while True:
        await asyncio.sleep(1)
        await queue.put(i)
        i += 1

async def consumer():
    while True:
        result = await queue.get()
        if result % 2 == 0:
            print(result, "is even!")
        else:
            print(result, "is odd!")
        await asyncio.sleep(4)
    
loop.create_task(produce_num())
loop.create_task(produce_num())
loop.create_task(consumer())
loop.create_task(consumer())
loop.create_task(consumer())
loop.create_task(consumer())

loop.run_forever()
    

