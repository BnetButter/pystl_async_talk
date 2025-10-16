import tkinter as tk
import asyncio
import websockets
import logging
import sys

stream_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
stream_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)  # or INFO, WARNING, etc.
logger.addHandler(stream_handler)

loop = asyncio.get_event_loop()

## handle sockets
clients = set()
async def ws_handler(client):
    clients.add(client)
    try:    
        async for message in client:
            logger.info(message)
    finally:
        clients.remove(client)
        



app = tk.Tk()

async def mainloop():
    async with websockets.serve(ws_handler, "0.0.0.0", "8765"):
        while True:
            app.update()
            await asyncio.sleep(0.01)


def main():

    loop.create_task(mainloop())
    loop.run_forever()
    

    

if __name__ == "__main__":
    main()