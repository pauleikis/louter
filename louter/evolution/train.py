import random

from louter.core.criteria import pauleikis_criteria
from louter.core.keyboard import ANSI, Ergodox
from louter.core.keycaps import ansi_with_lt, ansi_dvorak, ansi_colemak, ansi_workman, RandomKeyCaps, generate_new_random_ergodox

POOL_SIZE = 100

def init():
    result = []
    for _ in range(POOL_SIZE - len(result)):
        result += [generate_new_random_ergodox()]
    return sorted(pauleikis_criteria(keycaps=kc) for kc in result)


def breed(pool):
    pool = sorted(pool)
    offsprings = []
    for kb in pool[:20]:
        offsprings.append((kb @ random.choice(pool)))
        offsprings.append((kb @ random.choice(pool)) >> 2)
        offsprings.append((kb @ random.choice(pool)) >> 4)
        offsprings.append((kb @ random.choice(pool)) >> 7)

    return sorted(pool + offsprings)[:POOL_SIZE]


def evolve():
    pool = init()
    for idx in range(100):
        if not idx % 1:
            print(f"{idx:>5}: {sum(pool):14,.4f}")
        pool = breed(pool)
    return pool

def main():
    pool = evolve()
    print(pool[0])
    print(pool[1])
    print(pool[2])
    print(pool[3])


if __name__ == '__main__':
    main()
