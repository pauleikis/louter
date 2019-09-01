import random
from itertools import islice
from math import e
from functools import partial
import sys

import numpy as np

from louter.core.criteria import pauleikis_criteria
from louter.core.keyboard import Planck
from louter.core.keycaps import RandomKeyCaps, KeyCaps
from louter.util.softmax import soft_random_generator

POOL_SIZE = 30

new_planck = partial(KeyCaps, keyboard=Planck)


def init():
    if len(sys.argv) > 1:
        result = [new_planck(kb) for kb in sys.argv[1:]]
        generate_new_random = partial(RandomKeyCaps, sys.argv[1], Planck)
    else:
        result = []
        generate_new_random = partial(RandomKeyCaps, "◆YOUH  CDBW◆◆IAER FSTNK◆◆QXZL JVMPG◆◆◆◆◆◆◆◆◆◆◆◆", Planck)
    for _ in range(POOL_SIZE - len(result)):
        result += [generate_new_random()]
    return sorted(pauleikis_criteria(keycaps=kc) for kc in result)


def breed(pool):
    pool = sorted(pool)
    size = len(pool)
    offsprings = []
    generator = soft_random_generator(pool, t=-.2*(POOL_SIZE/size))
    for m, f in islice(zip(generator, generator), size):
        offsprings.append((m @ f) >> np.random.poisson(max(1, int(size / 3))))
    for x in islice(generator, size):
        offsprings.append(x >> np.random.poisson(max(1, int(size / 3))))
    for x in pool:
        offsprings.append(x >> np.random.poisson(max(1, int(size / 3))))

    return sorted(set(pool + offsprings))[:size]


def evolve():
    pool = init()
    print(pool[0])
    best = pool[0]()
    idx = 0
    checkpoint = idx 
    try:
        while len(pool) > 2:
            pool = breed(pool)
            print(f"{idx:>5} - pool size: {len(pool):>3} - total pool: {sum(pool):15,.2f} - best: {pool[0]():12,.4f} - worst: {pool[-1]():12,.4f}", end="\r")
            candidate = pool[0]()
            if candidate < best:
                best = candidate
                checkpoint = idx
                print(" " * 100, end="\r")
                print(idx, len(pool))
                print(pool[0])
            if idx - ((POOL_SIZE + 10) / len(pool)) ** e > checkpoint:
                checkpoint = idx  
                pool = pool[:-1]
            idx += 1
    except KeyboardInterrupt:
        print()
        print(pool[0])
        raise
    return pool


def main():
    pool = evolve()
    # print(" " * 100, end="\r")
    with open('results', 'aw') as out:
        out.write(pool[0])
    print(pool[0])


if __name__ == '__main__':
    with open('results', 'aw') as out:
        out.write('test\n')
    main()
