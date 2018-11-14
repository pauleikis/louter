import random
from itertools import islice

import numpy as np

from louter.core.criteria import english_criteria
from louter.core.keyboard import ANSI
from louter.core.keycaps import generate_new_random_ansi_english
from louter.util.softmax import soft_random_generator

POOL_SIZE = 100
ITERATIONS = 40
MEAN_MUTATIONS = 5
CROSSOVERS_PER_ITERATION = int(POOL_SIZE ** 1.3)


def init():
    result = []
    for _ in range(POOL_SIZE - len(result)):
        result += [generate_new_random_ansi_english()]
    return sorted(english_criteria(keycaps=kc) for kc in result)


def breed(pool):
    pool = sorted(pool)
    offsprings = []
    generator = soft_random_generator(pool)
    for m, f in islice(zip(generator, generator), CROSSOVERS_PER_ITERATION):
        offsprings.append((m @ f) >> np.random.poisson(MEAN_MUTATIONS))

    return sorted(set(pool + offsprings))[:POOL_SIZE]


def evolve():
    pool = init()
    try:
        for idx in range(ITERATIONS):
            if not idx % 1:
                print(f"{idx:>5} - total pool: {sum(pool):15,.2f} - best: {pool[0]():12,.4f} - worst: {pool[-1]():12,.4f}")
            if idx and not idx % 20:
                print(pool[0])
            pool = breed(pool)
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
