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
      


def sleep(time_s):
    start = time.time()
    while time.time() - start < time_s:
        yield



future = Future()

def set_future():
    yield from sleep(5)
    future.set_result("I have set a result here!")


def get_future_result():
    value = yield from future
    print("future value: ", value)


def interleave():
    i = 0
    while True:
        yield from sleep(1)
        print("interleave counter: ", i)
        i += 1

loop = EventLoop()
loop.create_task(set_future())
loop.create_task(get_future_result())
loop.create_task(interleave())
loop.run_forever()
