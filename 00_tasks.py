import asyncio

async def interleave1():
    while True:
        print("interleave1")
        await asyncio.sleep(1)

async def interleave2():
    while True:
        print("interleave2")
        await asyncio.sleep(1)

async def do_stack_overflow(stack_depth):
    print("current stack depth: ", stack_depth)
    await do_stack_overflow(stack_depth + 1)

async def dont_overflow(loop: asyncio.AbstractEventLoop, stack_depth):
    print("current stack depth:", stack_depth)
    loop.create_task(dont_overflow(loop, stack_depth+1))


def main():

    
    loop = asyncio.get_event_loop()
    t1 = loop.create_task(interleave1())
    t2 = loop.create_task(interleave2())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print(t1.get_stack())
        print(t2.get_stack())
    

    t1.cancel()
    
    input() # BLOCK the call

    


    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Demonstrating new callstack")

    t2.cancel()
    input() # BLOCK the call

    loop.create_task(do_stack_overflow(0))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        input("PAUSING LOOP")
    
    t = loop.create_task(dont_overflow(loop, 0))

    try:
        loop.run_forever()
    except:
        t.cancel()

    loop.run_forever()
    

if __name__ == "__main__":
    main()