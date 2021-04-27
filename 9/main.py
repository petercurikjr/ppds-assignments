from numba import cuda
import numpy
import math
import copy


@cuda.jit
def normalize(data, data_to_normalize):
    pos = cuda.grid(1)

    if pos < data.size:
        data_to_normalize[pos] = (data[pos] - min(data))/(max(data) - min(data))


def main():
    data = numpy.random.uniform(10, 1000, 128)
    data_to_normalize = copy.deepcopy(data)
    print(data)

    threads_per_block = 128
    blocks_per_grid = math.ceil(data.shape[0] / threads_per_block)
    print(len(data), '/', threads_per_block, '=', math.ceil(data.shape[0] / threads_per_block))

    normalize[blocks_per_grid, threads_per_block](data, data_to_normalize)
    print(data_to_normalize)


if __name__ == '__main__':
    main()
