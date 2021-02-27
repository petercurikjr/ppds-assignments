#MENO: PETER CURIK
from fei.ppds import Thread, Mutex


class Shared:
    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.array = [0] * self.end
        self.mutex = Mutex()


class Histogram(dict):
    def __init__(self, seq=[]):
        for item in seq:
            self[item] = self.get(item, 0) + 1


def counter(shared):
    while True:
        # toto riesenie sposobuje vylepsenie oproti prvemu, kde program na konci mohol padnut na IndexError
        # mutex ohranicil cele vnutro while cyklu
        # paralelizmus tu ale do vyraznej miery straca vyznam
        # v podstate skoro cela funkcia (co je hlavny bod programu) je limitovana na one thread at a time
        # vysledky su ale korektne, lebo kod je dokonale izolovany od vzajomneho rusenia sa vlakien medzi sebou
        # vsimnime si, ze sa unlock() vola aj pri splneni podmienky if
        # inak by nastal deadlock
        # pretoze prve vlakno by sice terminovalo while a skoncilo svoju pracu
        # no druhe vlakno by ostalo zamknute a nemal by ho kto "pustit dnu"
        shared.mutex.lock()
        if shared.counter >= shared.end:
            shared.mutex.unlock()
            break

        shared.array[shared.counter] += 1
        shared.counter += 1
        shared.mutex.unlock()


for _ in range(10):
    sh = Shared(1_000_000)
    t1 = Thread(counter, sh)
    t2 = Thread(counter, sh)

    t1.join()
    t2.join()

    print(Histogram(sh.array))
