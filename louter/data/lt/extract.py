from collections import Counter
from pathlib import Path

raw_dir = Path(__file__).parent

allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZĄČĘĖĮŠŲŪŽ"

count = 0

letters = Counter()
_2gram = Counter()
_3gram = Counter()

for line in open('/Users/paulius/Temp/trash/lt_text'):
    count += 1
    if not count % 1000:
        print(count)
    for word in line.split():
        sofar = '…'
        for letter in word.upper():
            if letter not in allowed_chars:
                sofar = ''
                continue
            letters[letter] += 1
            sofar += letter
            if len(sofar) > 1:
                _2gram[sofar[-2:]] += 1
            if len(sofar) > 2:
                _3gram[sofar[-3:]] += 1
        sofar += '…'
        if len(sofar) > 1:
            _2gram[sofar[-2:]] += 1
        if len(sofar) > 2:
            _3gram[sofar[-3:]] += 1

with open(raw_dir / "1grams.txt", "w") as out:
    total = sum(letters.values())
    for gram, count in letters.most_common():
        out.write(gram + ' ' + str(count / total) + '\n')

with open(raw_dir / "2grams.txt", "w") as out:
    total = sum(_2gram.values())
    for gram, count in _2gram.most_common():
        out.write(gram + ' ' + str(count / total) + '\n')

with open(raw_dir / "3grams.txt", "w") as out:
    total = sum(_3gram.values())
    for gram, count in _3gram.most_common():
        out.write(gram + ' ' + str(count / total) + '\n')

if __name__ == '__main__':
    pass