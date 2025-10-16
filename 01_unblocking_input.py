import asyncio

async def long_running_task():
    while True:
        print("I'm running")
        await asyncio.sleep(1)

async def mainloop(loop: asyncio.AbstractEventLoop):
    while True:
        my_input = await loop.run_in_executor(None, input)
        print(my_input)
        if my_input == "q":
            break
    input() # this will block the loop

def main():
    loop = asyncio.get_event_loop()
    loop.create_task(mainloop(loop))
    loop.create_task(long_running_task())

    # SSIGINT will stop mainloop but won't be propagated to child thread
    loop.run_forever()


if __name__ == "__main__":
    main()