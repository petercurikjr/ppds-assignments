from fei.ppds import Mutex, Semaphore, Thread, Event, print
from time import sleep
from random import randint


class Lightswitch:
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, sem):
        self.mutex.lock()
        counter = self.counter
        self.counter += 1
        if self.counter == 1:
            sem.wait()
        self.mutex.unlock()
        return counter

    def unlock(self, sem):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            sem.signal()
        self.mutex.unlock()


def init():
    access_data = Semaphore(1)
    turniket = Semaphore(1)
    ls_monitor = Lightswitch()
    ls_cidlo = Lightswitch()
    valid_data = Event()

    for monitor_id in range(8):
        Thread(monitor, monitor_id, valid_data, turniket, ls_monitor, access_data)
    for cidlo_id in range(3):
        Thread(cidlo, cidlo_id, turniket, ls_cidlo, valid_data, access_data)


def monitor(monitor_id, valid_data, turniket, ls_monitor, access_data):
    valid_data.wait()

    while True:
        turniket.wait()
        turniket.signal()

        pocet_citajucich_monitorov = ls_monitor.lock(access_data)
        trvanie_zapisu = randint(40,50)/1000

        print(f'monit "{monitor_id:02d}": '
              f'pocet_citajucich_monitorov={pocet_citajucich_monitorov:02d} '
              f'trvanie_citania={trvanie_zapisu:5.3f}')

        sleep(trvanie_zapisu)
        ls_monitor.unlock(access_data)


def cidlo(cidlo_id, turniket, ls_cidlo, valid_data, access_data):
    while True:
        sleep(randint(50,60)/1000)

        turniket.wait()
        pocet_zapisujucich_cidiel = ls_cidlo.lock(access_data)

        if cidlo_id == 2:
            trvanie_zapisu = randint(20,25)/1000
        else:
            trvanie_zapisu = randint(10,20)/1000
        turniket.signal()

        print(f'cidlo "{cidlo_id:02d}": '
              f'pocet_zapisujucich_cidiel={pocet_zapisujucich_cidiel:02d}, '
              f'trvanie_zapisu={trvanie_zapisu:5.3f}')
        sleep(trvanie_zapisu)

        ls_cidlo.unlock(access_data)
        valid_data.signal()


if __name__ == '__main__':
    init()
