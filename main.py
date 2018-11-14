from louter.evolution.train import evolve


def main():
    pool = evolve()
    print(pool[0])
    print(pool[1])
    print(pool[2])
    print(pool[3])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        exit(e)
