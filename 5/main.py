from fei.ppds import Semaphore, Mutex, Thread, print, Event
from random import randint
from time import sleep
import math


"""M a N su parametre modelu, nie synchronizacie ako takej.
Preto ich nedavame do zdielaneho objektu.
    M - pocet porcii misionara, ktore sa zmestia do hrnca.
    N - pocet divochov v kmeni
    C - pocet kucharov, ktori varia divochom
"""
M = 20
N = 4
C = 3


class SimpleBarrier:
    def __init__(self, size):
        self.size = size
        self.mutex = Mutex()
        self.cnt = 0
        self.sem = Semaphore(0)

    def wait(self,
             print_str,
             savage_id,
             print_last_thread=False,
             print_each_thread=False):
        self.mutex.lock()
        self.cnt += 1
        if print_each_thread:
            print(print_str % (savage_id, self.cnt))
        if self.cnt == self.size:
            self.cnt = 0
            if print_last_thread:
                print(print_str % (savage_id))
            self.sem.signal(self.size)
        self.mutex.unlock()
        self.sem.wait()


class Shared:
    def __init__(self):
        self.mutex = Mutex()
        self.mutex_cook = Mutex()
        self.servings = 0

        self.start_eating = Semaphore(0)
        self.start_cooking = Event()
        self.did_announce = False

        self.barrier1 = SimpleBarrier(N)
        self.barrier2 = SimpleBarrier(N)
        self.barrier_cooks = SimpleBarrier(C)


def get_serving_from_pot(savage_id, shared):
    print("divoch %2d: beriem si porciu" % savage_id)
    shared.servings -= 1


def eat(savage_id):
    print("divoch %2d: hodujem" % savage_id)
    # Zjedenie porcie misionara nieco trva...
    sleep(0.2 + randint(0, 3) / 10)


def savage(savage_id, shared):
    # stretnu a pockaju sa iba pred zacatim "party", toto nemusi byt vo while
    shared.barrier1.wait(
        "divoch %2d: prisiel som na veceru, uz nas je %2d",
        savage_id,
        print_each_thread=True)
    shared.barrier2.wait("divoch %2d: uz sme vsetci, zaciname vecerat",
                         savage_id,
                         print_last_thread=True)

    while True:
        shared.mutex.lock()
        print("divoch %2d: pocet zostavajucich porcii v hrnci je %2d" %
              (savage_id, shared.servings))

        # divosi idu po jednom a kontroluju stav hrnca
        if shared.servings == 0:
            print("divoch %2d: budim kucharov" % savage_id)
            # nastava udalost pre kucharov
            shared.start_cooking.signal()
            # divoch sa pozastavi a tym aj cela fronta za nim co caka pred KO
            shared.start_eating.wait()
        get_serving_from_pot(savage_id, shared)
        shared.mutex.unlock()

        eat(savage_id)


def put_servings_in_pot(shared, t, cook_id):
    """
    nejake minimum to bude vzdy trvat (0.5), mozeme si pod tym predstavit
    napr zovretie vody na 100 stupnov, cas kym sa uvari samotne maso...
    tieto veci nevie zrychlit hocikolko n kucharov
    """
    print("kuchar %2d: varim" % cook_id)
    sleep(t if t >= 0.5 else 0.5)


def cook(shared, cook_id):
    # cim viac kucharov, tym rychlejsi cely tim
    # vztah je vyjadreny logaritmickou funkciou
    worst_time = 8
    log_multiplier = 2
    efficiency = math.log(C)*log_multiplier
    t = randint(worst_time-2, worst_time) - efficiency

    while True:
        # cakaju na udalost
        shared.start_cooking.wait()
        shared.did_announce = False
        put_servings_in_pot(shared, t, cook_id)

        # pockaju sa kym vsetci dokoncia svoje ulohy
        shared.barrier_cooks.wait("kuchar %2d: dovarili vsetci kuchari", cook_id, print_last_thread=True)

        # po jednom vstupuju do KO a prvy z kucharov pusti divochov
        # nasledne vsetky vlakna sa dostanu na zaciatok while cyklu kde opat cakaju
        shared.mutex_cook.lock()
        if not shared.did_announce:
            shared.servings = M

            shared.start_eating.signal()
            shared.did_announce = True
            shared.start_cooking.clear()
        shared.mutex_cook.unlock()


def init_and_run():
    savages_threads = list()
    cooks_threads = list()

    shared = Shared()
    for savage_id in range(0, N):
        savages_threads.append(Thread(savage, savage_id, shared))

    for cook_id in range(0, C):
        cooks_threads.append(Thread(cook, shared, cook_id))

    for t in savages_threads + cooks_threads:
        t.join()


if __name__ == "__main__":
    init_and_run()
