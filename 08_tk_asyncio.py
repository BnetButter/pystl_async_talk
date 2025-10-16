import tkinter as tk
import asyncio
 
app = tk.Tk()
loop = asyncio.get_event_loop()
button = tk.Button(app, text="button")

button["command"] = lambda: button.configure(text="hello")
button.pack()


async def mainloop():
    while True:
        app.update()
        await asyncio.sleep(0.001)


def main():
    loop.create_task(mainloop())
    loop.run_forever()

main()