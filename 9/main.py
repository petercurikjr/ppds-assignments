"""
MENO: PETER CURIK

Experiment bol vykonavany pomocou emulatora. Pouzivatel si na demonstraciu rychlosti moze nastavit
velkost pola na ovela vacsie hodnoty (za predpokladu, ze planuje pouzit fyzicke GPU zariadenie).
Experiment sluzi cisto na demonstraciu pouzivania numba kniznice; v praxi je cielom pouzivat GPU
na vypoctovo narocne a rozsiahle ulohy.
"""

from numba import cuda
import numpy
import math
import copy


@cuda.jit
def normalize(data, data_to_normalize):
    """
    Kernel funkcia vykonavana na GPU. Pre vstupne data vytvori normalizovanu verziu.
    Tuto funkciu vykonava mnoho threadov paralelne.

    :param data: povodne data.
    :param data_to_normalize: data, ktore budu normalizovanou verziou povodnych dat.
    :return: nic; ide o kernel funkciu.
    """

    # ziskanie pozicie threadu (1D)
    pos = cuda.grid(1)

    # kontrola, ktora znemozni nadbytocnym threadom pracovat s prvkami mimo rozsahu pola
    if pos < data.size:
        data_to_normalize[pos] = (data[pos] - min(data)) / (max(data) - min(data))


def main():
    """
    Main funkcia inicializujuca vsetky potrebne udaje k vypoctu.

    :return: nic
    """

    # data generujeme nahodne z daneho rozsahu a poctu
    data = numpy.random.uniform(10, 1000, 128)
    data_to_normalize = copy.deepcopy(data)
    print('------------------------------------------------------------------')
    print('Input data:', data)

    # pozn.: v tomto pripade nema zmysel, aby bolo vlakien viac ako je velkost pola
    threads_per_block = 128
    # vypocet potrebnych blokov v gride
    blocks_per_grid = math.ceil(data.shape[0] / threads_per_block)

    print('------------------------------------------------------------------')
    print('Input_array_length / Threads_per_block = Blocks_per_grid')
    print(len(data), '/', threads_per_block, '=', math.ceil(data.shape[0] / threads_per_block))
    print('------------------------------------------------------------------')

    # spustenie kernel funkcie z CPU. vykonavana bude na GPU/emulatore
    normalize[blocks_per_grid, threads_per_block](data, data_to_normalize)
    print('Normalized data:', data_to_normalize)


if __name__ == '__main__':
    main()
