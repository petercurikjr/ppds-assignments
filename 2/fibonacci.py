from fei.ppds import Thread, Mutex, Event
from time import sleep
from random import randint


class Shared:
    def __init__(self):
        self.fib_arr = [0,1]
        self.m = Mutex()
        self.e = Event()

    def fibonacci(self, i):
        sleep(randint(1, 10) / 10)

        while True:
            #self.m.lock()
            if i+2 == len(self.fib_arr):
                break
            self.e.wait()
            #self.m.unlock()

        self.fib_arr.append(self.fib_arr[i] + self.fib_arr[i + 1])
        #self.m.unlock()
        self.e.signal()
        self.e.clear()
        print(self.fib_arr)


threads_num = 10
obj = Shared()
threads = list()
for i in range(threads_num):
    t = Thread(obj.fibonacci, i)
    threads.append(t)

for thread in threads:
    thread.join()