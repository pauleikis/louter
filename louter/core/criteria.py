from collections import Counter
from functools import partial
from math import e
from itertools import combinations
from pathlib import Path

from louter.core.keycaps import KeyCaps

# used get badness in decent range like ~ [1, 10] for visual representation, does not affect results
from louter.util.debug import trace

MULTIPLIER = 100 * e  # why e? because why not!
PATH_TO_DATA = Path(__file__).parent.parent / 'data'

inward_rolls = set(combinations('prmit', 3)) | set(combinations('PRMIT', 3)) | set(combinations('prmit', 2)) | set(combinations('PRMIT', 2))
outward_rolls = set(combinations('timrp', 3)) | set(combinations('TIMRP', 3)) | set(combinations('timrp', 2)) | set(combinations('TIMRP', 2))
same_finger_penalty = {k: p for k, p in zip("prmitPRMIT", [5, 2, 1.3, 1.2, 1.5] * 2)}
left_hand = "prmit"


class Criterion:

    def __call__(self, keycaps):
        return 0

    def __str__(self):
        return self.__class__.__name__

    def __eq__(self, other):
        return type(self) is type(other)


class FrequencyStrainCriterion(Criterion):
    freqs = None
    freqs2 = None
    freqs3 = None

    def __init__(self, freqs, freqs2, freqs3) -> None:
        super().__init__()
        self.freqs = freqs
        self.freqs2 = freqs2
        self.freqs3 = freqs3

    def __call__(self, keycaps):
        if keycaps.badness.get(self.__class__.__qualname__) is None:
            result = self.single_letter_badness(keycaps)
            result += self.gram2_badness(keycaps)
            result += self.gram3_badness(keycaps)
            keycaps.badness[self.__class__.__qualname__] = result / sum(keycaps.keyboard.strain) * MULTIPLIER
        return keycaps.badness[self.__class__.__qualname__]

    def single_letter_badness(self, keycaps):
        result = sum(keycaps.strain.get(key, 0) * self.freqs.get(key, 0) for key in keycaps.keycaps)
        result /= sum(self.freqs.values())
        return result

    def gram2_badness(self, keycaps):
        result = 0
        for gram, freq in self.freqs2.items():
            strain = keycaps.strain[gram[0]]
            fingers = keycaps.fingers[gram[0]], keycaps.fingers[gram[1]]
            if fingers[0] == fingers[1]:
                multiplier = same_finger_penalty[fingers[0]]
            elif fingers in inward_rolls:
                multiplier = 0.6
            elif fingers in outward_rolls:
                multiplier = 0.9
            elif (fingers[0] in left_hand) != (fingers[1] in left_hand):
                multiplier = 0.5
            else:
                multiplier = 1
            strain += keycaps.strain[gram[1]] * multiplier
            strain *= freq
            result += strain
        return result / 2

    def gram3_badness(self, keycaps):
        result = 0
        count = 0
        for gram, freq in self.freqs3.items():
            count += 1
            strain = keycaps.strain[gram[0]]
            fingers = keycaps.fingers[gram[0]], keycaps.fingers[gram[1]], keycaps.fingers[gram[2]]
            multiplier = 1
            if fingers[0] == fingers[1]:
                multiplier *= same_finger_penalty[fingers[1]]
            if fingers[1] == fingers[2]:
                multiplier *= same_finger_penalty[fingers[1]]
            if fingers[0] == fingers[1] == fingers[2]:
                multiplier *= same_finger_penalty[fingers[0]]
            elif fingers in inward_rolls:
                multiplier *= 0.6
            elif fingers in outward_rolls:
                multiplier *= 0.9
            else:
                if (fingers[0] in left_hand) != (fingers[1] in left_hand):
                    multiplier *= 0.7
                if (fingers[1] in left_hand) != (fingers[2] in left_hand):
                    multiplier *= 0.7
            strain += (keycaps.strain[gram[1]] + keycaps.strain[gram[2]]) * multiplier
            strain *= freq
            result += strain
        return result / 3


class LT(FrequencyStrainCriterion):
    def __init__(self, valid_chars):
        if not LT.freqs:
            freqs = {}
            for line in open(PATH_TO_DATA / 'lt' / '1grams.txt'):
                gram, freq = line.split()
                if all(l in valid_chars for l in gram):
                    freqs[gram] = float(freq)
            LT.freqs = freqs

        if not LT.freqs2:
            freqs = {}
            for line in open(PATH_TO_DATA / 'lt' / '2grams.txt'):
                gram, freq = line.split()
                if all(l in valid_chars for l in gram):
                    freqs[gram] = float(freq)
            LT.freqs2 = freqs
        if not LT.freqs3:
            freqs = {}
            for line in open(PATH_TO_DATA / 'lt' / '3grams.txt'):
                gram, freq = line.split()
                if all(l in valid_chars for l in gram):
                    freqs[gram] = float(freq)
                freqs[gram] = float(freq)
            LT.freqs3 = freqs

        super().__init__(LT.freqs, LT.freqs2, LT.freqs3)


class EN(FrequencyStrainCriterion):

    def __init__(self, valid_chars) -> None:
        if not EN.freqs:
            freqs = {}
            for line in open(PATH_TO_DATA / 'en' / '1grams.txt'):
                gram, freq = line.split()
                if all(l in valid_chars for l in gram):
                    freqs[gram] = float(freq)
            EN.freqs = freqs
        if not EN.freqs2:
            freqs = {}
            for line in open(PATH_TO_DATA / 'en' / '2grams.txt'):
                gram, freq = line.split()
                if all(l in valid_chars for l in gram):
                    freqs[gram] = float(freq)
            EN.freqs2 = freqs
        if not EN.freqs3:
            freqs = {}
            for line in open(PATH_TO_DATA / 'en' / '3grams.txt'):
                gram, freq = line.split()
                if all(l in valid_chars for l in gram):
                    freqs[gram] = float(freq)
            EN.freqs3 = freqs

        super().__init__(EN.freqs, EN.freqs2, EN.freqs3)


class Criteria:
    badness = None

    def __init__(self, *criteria, keycaps: KeyCaps, powers=None):
        if not powers:
            powers = [e] * len(criteria)
        assert len(powers) == len(criteria)
        self.criteria = [c(keycaps.strain.keys()) if type(c) is type else c for c in criteria]
        self.powers = powers
        self.keycaps = keycaps

    def __call__(self):
        if self.badness is None:
            self.badness = sum(c(self.keycaps) ** p for c, p in zip(self.criteria, self.powers))
        return self.badness

    def __matmul__(self, other):
        assert type(self) is type(other)
        assert self.criteria == other.criteria
        assert self.powers == other.powers
        return Criteria(*self.criteria, keycaps=self.keycaps @ other.keycaps, powers=self.powers)

    def __rshift__(self, other):
        return Criteria(*self.criteria, keycaps=self.keycaps >> other, powers=self.powers)

    def __str__(self):
        result = str(self.keycaps)
        result += '\n'
        for criterion in self.criteria:
            result += f"{criterion!s:>12}: {criterion(self.keycaps):12.4f}"
            result += '\n'
        result += f"{'TOTAL':>12}: {self():12.4f}"
        return result

    def __lt__(self, other):
        if isinstance(other, Criteria):
            return self() < other()
        return self() < other

    def __add__(self, other):
        if isinstance(other, Criteria):
            return self() + other()
        return self() + other

    def __radd__(self, other):
        if isinstance(other, Criteria):
            return self() + other()
        return self() + other

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        assert self.criteria == other.criteria
        assert self.powers == other.powers
        return self.keycaps == other.keycaps

    def __hash__(self):
        return hash(self.keycaps)


pauleikis_criteria = partial(Criteria, LT, EN)
english_criteria = partial(Criteria, EN)


if __name__ == '__main__':
    from louter.core.keyboard import Ergodox, ANSI

    a = KeyCaps("◆◆ ĄX◆◆◆◆ČŠQ◆◆◆ŪBOGŲWPSJZ◆◆◆ĘHDIAĖFNLMK ◆◆◆Y◆ĮECVTŽ◆◆◆◆◆◆◆◆◆◆◆UR◆◆◆◆◆◆◆◆◆◆◆◆", Ergodox)
    b = KeyCaps("◆◆ ĄX◆◆◆◆ČŠQ◆◆◆ŪBOGŲWPSJZ◆◆◆ĘHDIAĖFNLMK ◆◆◆Y◆ĮECVTŽ◆◆◆◆◆◆◆◆◆◆◆UR◆◆◆◆◆◆◆◆◆◆◆◆", Ergodox)


    # z = KeyCaps("◆◆QŲŪ◆◆◆◆ĖXW◆◆◆ĮRGKŠĘDNYŽ◆◆◆ZJISMĄBOLHCČ◆◆◆F◆◆AVPU◆◆◆◆◆◆◆◆◆◆◆◆TE◆◆◆◆◆◆◆◆◆◆◆◆", Ergodox)
    print(pauleikis_criteria(keycaps=a))
    # print(pauleikis_criteria(keycaps=b))
