from louter.evolution.train import evolve


def main():
    pool = evolve()
    # print()
    # print(pool[0])
    with open('results', 'a') as out:
    	out.write(str(pool[0]))
    	out.write('\n')
    # for idx, kb in enumerate(pool):
    #     print(idx + 1)
    #     print(kb)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        exit(e)
