import random
from itertools import islice

import numpy as np

from louter.core.criteria import pauleikis_criteria
from louter.core.keyboard import ANSI, Ergodox
from louter.core.keycaps import ansi_with_lt, ansi_dvorak, ansi_colemak, ansi_workman, RandomKeyCaps, generate_new_random_ergodox, generate_new_preferred_ergodox
from louter.util.softmax import soft_random_generator

POOL_SIZE = 60
# ITERATIONS = 100
MEAN_MUTATIONS = 2
CPI_POWER = 2


def init():
    result = []
    for _ in range(POOL_SIZE - len(result)):
        result += [generate_new_preferred_ergodox()]
    return sorted(pauleikis_criteria(keycaps=kc) for kc in result)


def breed(pool):
    pool = sorted(pool)
    size = len(pool)
    offsprings = []
    generator = soft_random_generator(pool, t=-.2*(POOL_SIZE/size))
    for m, f in islice(zip(generator, generator), size):
        offsprings.append((m @ f) >> np.random.poisson(max(1, int(size / 10))))
    for x in islice(generator, size):
        offsprings.append(x >> np.random.poisson(max(1, int(size / 10))))
    for x in pool:
        offsprings.append(x >> np.random.poisson(max(1, int(size / 10))))

    return sorted(set(pool + offsprings))[:size - (random.random() < (size - 0.9)/(POOL_SIZE * 4))]


def evolve():
    pool = init()
    try:
        idx = 0
        while len(pool) > 3:
            if not idx % 1:
                print(f"{idx:>5} - pool size: {len(pool):>3} - total pool: {sum(pool):15,.2f} - best: {pool[0]():12,.4f} - worst: {pool[-1]():12,.4f}")
            if idx and not idx % 10:
                print(pool[0])
            pool = breed(pool)
            idx += 1
    except KeyboardInterrupt:
        print()
        print(pool[0])
        print(pool[1])
        print(pool[2])
        raise
    return pool


def main():
    pool = evolve()
    print(pool[0])
    print(pool[1])
    print(pool[2])


if __name__ == '__main__':
    main()
