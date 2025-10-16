import asyncio
import random

lock = asyncio.Lock()

async def produce_rng():
    await asyncio.sleep(0.25)
    return random.choice([i for i in range(10)])

async def waiter1():
    while True:
        while (await produce_rng()) != 4: 
            pass

        async with lock:
            print("Found 4!")

            while (await produce_rng()) != 3:
                pass
            else:
                print("3")
            while (await produce_rng()) != 2:
                pass
            else:
                print("2")
            
            while (await produce_rng()) != 1:
                pass
            else:
                print(1)
            
    

async def waiter2():
    while True:
        while (await produce_rng()) != 6:
            pass
        async with lock:
            print("Found 6!")

            while (await produce_rng()) != 7:
                pass
            else:
                print("7")
    
            while (await produce_rng()) != 8:
                pass
            else:
                print("8")
            
            while (await produce_rng()) != 9:
                pass
            else:
                print("9")
                
loop = asyncio.get_event_loop()
loop.create_task(waiter1())
loop.create_task(waiter2())
loop.run_forever()
