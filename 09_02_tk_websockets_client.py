import asyncio
import tkinter as tk
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
app = tk.Tk()
app.geometry("400x400")

connection_label = tk.Label(app, text="Not connected")
connection_label.pack()

async def mainloop():
    while True:
        app.update()
        await asyncio.sleep(0.01)

client_ptr = [ None ]
connection_condition = asyncio.Condition()

async def connection_loop():
    while True:
        logger.info(f"trying to connect...")
        try:
            async with websockets.connect("ws://localhost:8765") as ws:
                async with connection_condition:
                    client_ptr[0] = ws
                    connection_condition.notify_all()

                logger.info(f"Server connected")

                while True:
                    await ws.ping()
                    await asyncio.sleep(1)

        except (OSError, websockets.exceptions.ConnectionClosed):
            logger.info(f"Server disconnected")
            async with connection_condition:
                client_ptr[0] = None
                connection_condition.notify_all()
        
            await asyncio.sleep(5)
        


async def update_connection_status():
    while True:
        async with connection_condition:
            await connection_condition.wait()
            if client_ptr[0] is None:
                connection_label["text"] = "Not connected"
            else:
                connection_label["text"] = "Connected"


async def send_messages_while_connection_active():
    while True:
        async with connection_condition:
            await connection_condition.wait_for(lambda: client_ptr[0] is not None)
            ws = client_ptr[0]
            await ws.send("HELLO WORLD")
            logger.info(f"sent client message")

        await asyncio.sleep(1)



def main():
    loop.create_task(connection_loop())
    loop.create_task(mainloop())
    loop.create_task(update_connection_status())
    loop.create_task(send_messages_while_connection_active())
    loop.run_forever()

if __name__ == "__main__":
    main()