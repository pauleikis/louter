import wordfreq
from collections import Counter


def main():
    letters = Counter()
    _2gram = Counter()
    _3gram = Counter()

    for word, freq in wordfreq.get_frequency_dict('en', wordlist='best').items():
        sofar = '…'  # we're including space at the beginning of the word
        for letter in word.upper():
            if letter not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                sofar = ''
                continue
            letters[letter] += freq / (len(word))
            sofar += letter
            if len(sofar) > 1:
                _2gram[sofar[-2:]] += freq / (len(word) + 1)
            if len(sofar) > 2:
                _3gram[sofar[-3:]] += freq / (len(word))

        sofar += '…'
        if len(sofar) > 1:
            _2gram[sofar[-2:]] += freq / (len(word) + 1)
        if len(sofar) > 2:
            _3gram[sofar[-3:]] += freq / (len(word))

    with open("1grams.txt", "w") as out:
        for gram, count in letters.most_common():
            out.write(gram + ' ' + str(count) + '\n')

    with open("2grams.txt", "w") as out:
        for gram, count in _2gram.most_common():
            out.write(gram + ' ' + str(count) + '\n')

    with open("3grams.txt", "w") as out:
        for gram, count in _3gram.most_common(6000):
            out.write(gram + ' ' + str(count) + '\n')


if __name__ == '__main__':
    main()
