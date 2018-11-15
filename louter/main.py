from louter.evolution.train import evolve


def main():
    pool = evolve()
    for idx, kb in enumerate(pool):
        print(idx)
        print(kb)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        exit(e)
