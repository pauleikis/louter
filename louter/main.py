
if __name__ == '__main__':
    result = 0
    for line in open("../3grams.txt"):
        result += int(line.split()[1])
    print(result)

    result = 0
    for line in open("../2grams.txt"):
        result += int(line.split()[1])
    print(result)

    print(result - 25187693)
