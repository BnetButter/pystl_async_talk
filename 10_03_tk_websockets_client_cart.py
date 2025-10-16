import asyncio
import tkinter as tk
import websockets
import logging
import sys
import aiohttp
import json
from tkinter import ttk

async def get(url: str, params: dict | None = None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            return await response.text()

# INIT LOGGING
stream_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
stream_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)  # or INFO, WARNING, etc.
logger.addHandler(stream_handler)

# INIT TK LOOP

loop = asyncio.get_event_loop()
app = tk.Tk()
order_frame = tk.Frame(app)
app.geometry("400x400")

connection_label = tk.Label(app, text="Not connected")
connection_label.pack()
order_frame.pack()

async def mainloop():
    while True:
        app.update()
        await asyncio.sleep(0.01)

client_ptr = [ None ]
connection_condition = asyncio.Condition()

async def recv_message():
    while True:
        async with connection_condition:
            await connection_condition.wait_for(lambda: client_ptr[0] != None)
            ws = client_ptr[0]
            connection_condition.notify_all()
        
        
        try:
            # we want to release the lock while waiting on this message
            data = await ws.recv()
            logger.info(f"Event: " + data)
        except:
            async with connection_condition:
                client_ptr[0] = None
                connection_condition.notify_all()
            logger.error(f"ERROR in receive")
        else:
            if data == "new order":
                await update_orders()
        

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


async def update_orders():

    def create_order_complete(order):
        message_orders = ", ".join(order)
        def callback(*args):
            async def task():
                logger.info(f"Clicked")
                async with connection_condition:
                    await connection_condition.wait_for(lambda: client_ptr[0] is not None)
                    ws = client_ptr[0]
                    await ws.send(message_orders)
            
            loop.create_task(task())
        return callback


    data = json.loads(await get("http://localhost:8000/api/orders"))
    for widget in order_frame.winfo_children():
        widget.destroy()
    
    for order in data:
        group = tk.Frame(order_frame, bd=2, relief="ridge")
        group.bind('<Button-1>', create_order_complete(order))
        group.pack()

        for item in order:
            label = tk.Label(group, text=item)
            label.pack()


def main():
    loop.create_task(connection_loop())
    loop.create_task(mainloop())
    loop.create_task(update_connection_status())
    loop.create_task(update_orders())
    loop.create_task(recv_message())
    loop.run_forever()

if __name__ == "__main__":
    main()