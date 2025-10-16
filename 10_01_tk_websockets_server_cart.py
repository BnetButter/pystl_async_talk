import tkinter as tk
import asyncio
import websockets
import logging
import sys
import aiohttp



async def post(url: str, body: dict | None = None):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body) as response:
            return await response.text()

stream_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
stream_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)  # or INFO, WARNING, etc.
logger.addHandler(stream_handler)
messages = []
message_cond = asyncio.Condition()

loop = asyncio.get_event_loop()

## handle sockets
clients = set()
async def ws_handler(client):
    clients.add(client)
    try:
        async for message in client:
            logger.info(f"Received message: {message}")
            async with message_cond:
                messages.append(message)
                message_cond.notify_all()
    finally:
        clients.remove(client)


app = tk.Tk()
cart_lock = asyncio.Condition()

async def mainloop():
    async with websockets.serve(ws_handler, "0.0.0.0", "8765"):
        while True:
            app.update()
            await asyncio.sleep(0.01)



shopping_cart, menu = tk.Frame(app), tk.Frame(app)
shopping_cart.pack(side=tk.RIGHT)
menu.pack(side=tk.LEFT)

label = tk.Label(app)
label.pack(side=tk.BOTTOM)

async def update_label():
    while True:
        async with message_cond:
            await message_cond.wait()
            message = "\n".join(messages)
            label["text"] = message

loop.create_task(update_label())

shopping_cart_data = []
menu_items = [
    "Hamburger",
    "Soda",
    "Cheeseburger",
    "Pasta",
]


async def submit_order():
    async with cart_lock:
        await post("http://localhost:8000/api/orders", shopping_cart_data)
        for client in clients:
            await client.send("new order")
            logger.info(f"Alerted clients of new order")
        shopping_cart_data[:] = []
        cart_lock.notify_all()


post_order = tk.Button(app, text="Submit", command=lambda: loop.create_task(submit_order()))
post_order.pack()

# create callback for each item
def create_callback(item):
    def on_click(*args):
        async def on_click():
            async with cart_lock:
                shopping_cart_data.append(item)
                cart_lock.notify_all()
        loop.create_task(on_click())
    return on_click

for item in menu_items:
    button = tk.Button(menu, text=item, command=create_callback(item))
    button.pack()

async def update_cart():

    def create_delete_function(index):
        def onclick(*args):
            async def coro():
                async with cart_lock:
                    del shopping_cart_data[index]
                    cart_lock.notify_all()
            loop.create_task(coro())
        return onclick


    while True:
        async with cart_lock:
            await cart_lock.wait()

            for widget in shopping_cart.winfo_children():
                widget.destroy()
            
            for i, item in enumerate(shopping_cart_data):
                frame = tk.Frame(shopping_cart)
                tk.Label(frame, text=item).pack(side=tk.LEFT)
                tk.Button(frame, text="DEL", command=create_delete_function(i)).pack(side=tk.RIGHT)
                frame.pack()
                logger.info(f"CART: {shopping_cart_data}")

            shopping_cart.update()



def main():
    loop.create_task(mainloop())
    loop.create_task(update_cart())
    loop.run_forever()

if __name__ == "__main__":
    main()