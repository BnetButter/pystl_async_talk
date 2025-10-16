import threading
import asyncio
import time

loop = asyncio.get_event_loop()


def schedule_task_from_thread():
    async def worker():
        print("async task")
        await asyncio.sleep(2)
        print("OK")

    def print_error(task):
        if task.exception():
            print(task.exception())
        if task.done():
            print("DONE")

    time.sleep(2) # wait for event loop to start 
    t = loop.create_task(worker())
    print(t)
    t.add_done_callback(print_error)


def schedule_task_from_thread_safe():
    async def worker():
        print("async task")
        await asyncio.sleep(2)
        print("OK")

    time.sleep(2)
    print("schedule threadsafe")
    asyncio.run_coroutine_threadsafe(worker(), loop)

threading.Thread(target=schedule_task_from_thread).start()
#threading.Thread(target=schedule_task_from_thread_safe).start()
loop.run_forever()