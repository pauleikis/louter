from collections import Counter
from pathlib import Path

valid = "ĄČĘĖĮŠŲŪŽQWERTYUIOPASDFGHJKLZXCVBNM.,"


def main():
    result = Counter()
    for line in open(Path(__file__).parent / "bak" / "2grams.txt"):
        a, b = line.split()
        result[a] = int(b)
    total = sum(result.values())

    with open(Path(__file__).parent / "2grams.txt", 'w') as out:
        for k, v in result.most_common():
            if k[0] not in valid or k[1] not in valid:
                continue
            out.write(k)
            out.write(' ')
            out.write(str(v / total))
            out.write('\n')

    result = Counter()
    for line in open(Path(__file__).parent / "bak" / "3grams.txt"):
        a, b = line.split()
        result[a] = int(b)
    total = sum(result.values())

    with open(Path(__file__).parent / "3grams.txt", 'w') as out:
        for k, v in result.most_common(3000):
            if k[0] not in valid or k[1] not in valid or k[2] not in valid:
                continue
            out.write(k)
            out.write(' ')
            out.write(str(v / total))
            out.write('\n')


if __name__ == '__main__':
    main()
