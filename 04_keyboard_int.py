import asyncio
import time

async def handle_me():
    try:
        await asyncio.sleep(1000)
    except KeyboardInterrupt:
        print("handle_me")

async def handle_another_me():
    try:
        await time.sleep(1000)
    except KeyboardInterrupt:
        print("handle_another_me")


loop = asyncio.get_event_loop()
loop.create_task(handle_me())
loop.create_task(handle_another_me())
loop.run_forever()