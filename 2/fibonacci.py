"""
MENO: PETER CURIK

Odpovede na otazky:
1) Najmensi pocet je jeden. Napriklad jeden Mutex.
Moze byt v Shared triede a jeden objekt si budu zdielat vsetky vlakna
2) Pouzitie signalizacie: vlakno ktore pridalo prvok do pola da signal cakajucemu
vlaknu, ze moze pridat prvok do pola
Pouzitie rendezvous: vlakno A pocka pred kontrolovanim dlzky pola, kym vlakno B
prida novy prvok do pola
Pouzitie bariery: nevidim v tomto pripade vyuzitie
Pouzitie vzajomneho vylucenia: A nemoze kontrolovat dlzku pola, ked B do neho pridava
"""

from fei.ppds import Thread, Mutex, Event
from time import sleep
from random import randint


class Shared:
    """
    Trieda obsahujuca data ktore su zdielane napriec vlaknami.
    """

    def __init__(self):
        self.fib_arr = [0, 1]
        self.m = Mutex()
        self.e = Event()

    """
    Metoda prida dalsi clen Fibonacciho postupnosti do zdielaneho pola.
    
    Argumenty:
    self -- samotna instancia triedy Shared
    i -- identifikator vlakna
    
    Metoda implementuje Mutex a Event.
    Mutex operuje v nekonecnom while cykle, povoluje if podmienku kontrolovat
    iba jednemu vlaknu v jednom case.
    Mutex je odomknuty este aj po pridani prvku postupnosti, aby dalsie cakajuce
    vlakna mohli dokoncit svoju pracu.
    
    Event nariaduje vsetkym vlaknam cakat vo while cykle pokial nesplnili podmienku.
    Vlakno ktore splni podmienku sa vyhne cakaniu. Namiesto toho prida prvok do pola
    a sposobi nastanie udalosti a nasledny clear. Dalsie vlakna mozu pokracovat.
    """

    def fibonacci(self, i):
        sleep(randint(1, 10) / 10)

        while True:
            # self.m.lock()
            if i + 2 == len(self.fib_arr):
                break
            self.e.wait()
            # self.m.unlock()

        self.fib_arr.append(self.fib_arr[i] + self.fib_arr[i + 1])
        # self.m.unlock()
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
