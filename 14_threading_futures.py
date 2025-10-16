import threading
import tkinter as tk
import time

class Future:

    def __init__(self):
        self._status = "Pending"
        self._result = None
    
    def set_result(self, value):
        self._status = "Done"
        self._result = value
    
    def __iter__(self):
        return self

    def __next__(self):
        if self._status == "Done":
            raise StopIteration(self._result)


class EventLoop:

    def __init__(self):
        self.tasks = set()
    
    def create_task(self, generator):
        self.tasks.add(generator)

    def run_forever(self):    
        while True:
            for task in list(self.tasks):
                try:
                    next(task)
                except StopIteration:
                    self.tasks.remove(task)
    

    def run_in_executor(self, executor, blocking_func):
        future = Future()
        def worker():
            result = blocking_func()
            future.set_result(result)
        threading.Thread(target=worker).start()
        return future

def sleep(time_s):
    start = time.time()
    while time.time() - start < time_s:
        yield


app = tk.Tk()
app.geometry("800x600")

label = tk.Label(app)
label.pack()

stdin_input = tk.Label(app)
stdin_input.pack()

def update_stdin_text():
    while True:
        result = yield from loop.run_in_executor(None, input)
        stdin_input["text"] = result

def update_label():
    for i in range(100000000):
        yield from sleep(1)
        label["text"] = str(i)


def mainloop():
    while True:
        app.update()
        yield from sleep(0.01)


loop = EventLoop()
loop.create_task(mainloop())
loop.create_task(update_label())
loop.create_task(update_stdin_text())
loop.run_forever()

