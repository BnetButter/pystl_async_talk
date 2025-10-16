import time

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

def sleep(time_s):
    start = time.time()
    while time.time() - start < time_s:
        yield


def interleave1():
    while True:
        yield from sleep(1)
        print("hello")

def interleave2():
    while True:
        yield from sleep(5)
        print("world")

def short_task():
    yield from sleep(10)
    print("done")



loop = EventLoop()
loop.create_task(interleave1())
loop.create_task(interleave2())
loop.create_task(short_task())

loop.run_forever()