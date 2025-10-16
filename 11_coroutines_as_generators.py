import time

def generator():
    for i in range(5):
        yield i
    
    return "Done"
 
g = generator()

while g:
    try:
        print(next(g))
    except StopIteration as e:
        print(e.value)
        break

input("Enter to continue")

def call_generator():
    first = yield from generator()
    print("yielded value first: ", first)
    second = yield from generator()
    print("yielded value second:", second)

    return "AFSDFSD IM DONE"


g = call_generator()

while True:
    try:
        print(next(g))
    except StopIteration as e:
        print("call generator value", e.value)
        break



def sleep(time_s):
    start = time.time()
    while time.time() - start < time_s:
        yield

input("enter to continue to demonstrate sleep")

sleep_coro = sleep(5)

while True:
    try:
        next(sleep_coro)
    except StopIteration:
        print("Waited 5 seconds done")
        break



