import asyncio
import threading

loop = asyncio.get_event_loop()
future = loop.create_future()


async def wait_for_input():
    user_input = await future
    print("print received resuponse: ", user_input)

def set_future():
    result = input("Enter some response")
    loop.call_soon_threadsafe(lambda: future.set_result(result))

threading.Thread(target=set_future).start()
loop.run_until_complete(wait_for_input())
