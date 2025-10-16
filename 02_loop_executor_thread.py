import threading
import asyncio


def blocking_task():
    tid = threading.current_thread()
    print(tid.ident)

async def coroutine(loop):
    await loop.run_in_executor(None, blocking_task)


def main():
    tid = threading.current_thread()
    print(tid.ident)
    loop = asyncio.get_event_loop()
    loop.create_task(coroutine(loop))
    loop.run_forever()

if __name__ == "__main__":
    main()