from collections import Counter

transmap = str.maketrans("ĄČĘĖĮŠŲŪŽ", "ACEEISUUZ")

counter = Counter()
for line in open("with_lt/1grams.txt"):
	letter, freq = line.split()
	letter, freq = letter.translate(transmap), float(freq)
	counter[letter] += freq

with open("1grams.txt", "w") as out:
	for item, freq in counter.most_common():
		out.write(f"{item} {freq}\n")

counter = Counter()
for line in open("with_lt/2grams.txt"):
	letter, freq = line.split()
	letter, freq = letter.translate(transmap), float(freq)
	counter[letter] += freq

with open("2grams.txt", "w") as out:
	for item, freq in counter.most_common():
		out.write(f"{item} {freq}\n")

counter = Counter()
for line in open("with_lt/3grams.txt"):
	letter, freq = line.split()
	letter, freq = letter.translate(transmap), float(freq)
	counter[letter] += freq

with open("3grams.txt", "w") as out:
	for item, freq in counter.most_common():
		out.write(f"{item} {freq}\n")