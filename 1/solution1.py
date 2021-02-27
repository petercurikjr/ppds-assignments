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
        if shared.counter >= shared.end:
            break

        # mutex v tomto rieseni izoluje iba cisto operacie s polom (najviac
        # jedno vlakno moze menit hodnoty pola a posunut sa v poli dalej)
        # takto zaistime to, ze sa nepreskoci inkrementacia niektorych hodnot na danych indexoch
        # pripadne, ze sa hodnota na danom indexe zvysi viackrat
        # po spusteni programu dostavame korektne hodnoty celeho pola

        # napriek tomu niekedy nastava chyba IndexError: list index out of range
        # preco? tu je dovod:
        # majme vlakna A a B
        # vlakno A je vpustene do casti kodu ktora je ohranicena mutexom a vykona instrukcie
        # vlakno B caka lebo zamok je stale locked
        # vlakno A dokonci instrukcie a odomkne zamok
        # no zaroven ide opat na zaciatok while cyklu a kontroluje podmienku
        # medzicasom ale vlakno B je vpustene do mutex ohranicenej casti
        # ak vlakno B stihne skor vykonat svoju cast nez A skontrolovat podmienku while cyklu
        # tak na konci pola nastava IndexError
        # ak vlakno A stihne zastavit while cyklus predtym, nez B inkrementuje index pola
        # tak sa program ukonci korektne a este aj bez IndexErroru
        shared.mutex.lock()
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
