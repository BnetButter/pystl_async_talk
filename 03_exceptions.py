import asyncio

async def throwing_an_error():
    raise Exception("I'm an error! Don't Retrieve me")

async def throwing_an_error_but_retrieve_me():
    raise Exception("OK do something with this")


async def handle_exception():
    print("Doing something to fix the problem")

def main():
    loop = asyncio.get_event_loop()

    
    loop.create_task(throwing_an_error())

    task = loop.create_task(throwing_an_error_but_retrieve_me())
    def on_complete(task:asyncio.Task):
        if task.exception():
            return loop.create_task(handle_exception())
    
    task.add_done_callback(on_complete)

 
    
    loop.run_forever()

if __name__ == "__main__":
    main()