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
    # toto riesenie je akysi "code cleanup" predchadzajucej verzie
    # pretoze funkcia counter() neobsahuje nic ine nez while cyklus
    # a teda umiestnenie lock(), unlock() na zaciatok a koniec while cyklu je z log. hladiska prakticky
    # to iste, nez umiestnenie lock(), unlock() na zaciatok a koniec samotnej funkcie
    # usetrili sme si jeden unlock(), ktory v predch. verzii musel byt aj v if scope
    # samozrejme vysledky su rovnake ako v predch. verzii
    # az na to, ze tato verzia zbehla najrychlejsie
    # pravdepodobne vie takymto sposobom interpreter efektivnejsie managovat vlakna
    shared.mutex.lock()
    while True:
        if shared.counter >= shared.end:
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
