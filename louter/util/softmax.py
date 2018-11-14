import random
from statistics import stdev
from math import exp


def weighted_choice(seq, weights):
    # try:
    assert len(weights) == len(seq)
    assert abs(1. - sum(weights)) < 1e-6
    # except AssertionError:
    #     for x in seq:
    #         print(x)
    #     print("-------------")
    #     for x in weights:
    #         print(x)
    #     raise

    x = random.random()
    for elmt, weight in zip(seq, weights):
        if x <= weight:
            return elmt
        x -= weight


def softmax(seq, t):
    try:
        t /= stdev(seq)
    except ZeroDivisionError:
        print(seq)
        raise
    zs = [exp(t * e) for e in seq]
    sum_z = sum(zs)
    return [z / sum_z for z in zs]


def soft_choice(seq, t=-1, weight_func=lambda x: x()):
    return weighted_choice(seq, softmax(map(weight_func, seq), t))


def soft_random_generator(seq, t=-1, weight_func=lambda x: x()):
    soft_distribution = softmax(list(map(weight_func, seq)), t)
    while True:
        yield weighted_choice(seq, soft_distribution)


if __name__ == '__main__':
    def softmax(seq, t):
        zs = [exp(t * e) for e in seq]
        sum_z = sum(zs)
        return [z / sum_z for z in zs]

    import statistics
    print(softmax([100, 200, 300], -1/statistics.stdev([100, 200, 300])))
    print(softmax([10, 20, 30], -1/statistics.stdev([10, 20, 30])))
    print(softmax([.1, .2, .3], -1/statistics.stdev([.1, .2, .3])))
    print()
    print(softmax([1, 2, 3], -1))
    print(softmax([11, 12, 13], -1))
    print(softmax([-1, 0, 1], -1))
    print()
    print('(╯°□°）╯︵ ┻━┻')