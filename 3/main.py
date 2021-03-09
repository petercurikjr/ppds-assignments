"""
MENO: PETER CURIK
ÚLOHA: PRODUCENT-KONZUMENT
"""

from fei.ppds import Mutex, Semaphore, Thread
from time import sleep
from random import randint
from typing import Callable
import matplotlib.pyplot as plt


class Lightswitch:
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, sem):
        self.mutex.lock()
        self.counter += 1
        if self.counter == 1:
            sem.wait()
        self.mutex.unlock()

    def unlock(self, sem):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            sem.signal()
        self.mutex.unlock()


class Shared:
    def __init__(self):
        self.finished = False
        self.counter = 0
        self.lock = Mutex()

    def produce(self):
        self.lock.lock()
        self.counter += 1
        self.lock.unlock()


def producer(items, free, shared: Shared, time_to_produce: Callable[[], float]):
    while True:
        sleep(time_to_produce())  # produce item
        free.wait()
        shared.produce()  # add item
        items.signal()
        if shared.finished:
            break


def consumer(items, free, shared: Shared, time_to_consume: Callable[[], float]):
    while True:
        items.wait()
        free.signal()  # get item
        sleep(time_to_consume())  # process item
        if shared.finished:
            break


def producer_consumer_experiment():
    results = []
    done = 0

    for time_to_produce in range(10):

        # for n_consumers in range(10, 21):
        for n_consumers in range(1, 11):

            items_per_second_sum = 0
            n_repetitions = 10
            for trial in range(n_repetitions):
                items = Semaphore(0)

                # free = Semaphore(10)
                free = Semaphore(20)

                shared = Shared()
                divider = 250
                [Thread(consumer, items, free, shared, lambda: randint(0, 10) / divider) for x in range(n_consumers)]

                [Thread(producer, items, free, shared, lambda: time_to_produce / divider) for x in range(10)]
                # [Thread(producer, items, free, shared, lambda: time_to_produce / divider) for x in range(20)]

                sleep_time = 0.05
                sleep(sleep_time)
                shared.finished = True
                items.signal(100)
                free.signal(100)

                n_produced_items = shared.counter
                items_per_second = n_produced_items / sleep_time
                items_per_second_sum += items_per_second

            average_items_per_second = items_per_second_sum / n_repetitions
            results.append((time_to_produce / divider, n_consumers, average_items_per_second))
            done += 1
            print(done, '%')

    plot(results)


def plot(results: list):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    x = [a[0] for a in results]
    y = [a[1] for a in results]
    z = [a[2] for a in results]
    ax.set_xlabel('cas produkcie (s)')
    ax.set_ylabel('pocet konzumentov')
    ax.set_zlabel('pocet vyrobkov za sekundu')
    ax.plot_trisurf(x, y, z, cmap='viridis', edgecolor='none')
    plt.show()


if __name__ == '__main__':
    producer_consumer_experiment()
