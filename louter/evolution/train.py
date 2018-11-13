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
        offsprings.append((kb @ random.choice(pool)) >> 1)
        offsprings.append((kb @ random.choice(pool)) >> 3)
        offsprings.append((kb @ random.choice(pool)) >> 7)

    return sorted(set(pool + offsprings))[:POOL_SIZE]


def evolve():
    pool = init()
    try:
        for idx in range(1000):
            if not idx % 1:
                print(f"{idx:>5} - total pool: {sum(pool):15,.2f} - best: {pool[0]():12,.4f} - worst: {pool[-1]():12,.4f}")
            if idx and not idx % 20:
                print(pool[0])
            pool = breed(pool)
    except KeyboardInterrupt:
        print()
        print(pool[0])
        raise
    return pool

def main():
    pool = evolve()
    print(pool[0])
    print(pool[1])
    print(pool[2])
    print(pool[3])


if __name__ == '__main__':
    main()
