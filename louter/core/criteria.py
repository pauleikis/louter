from collections import Counter, defaultdict
from functools import partial
from math import e, pi
from itertools import combinations
from pathlib import Path

from louter.core.keycaps import KeyCaps

# used get badness in decent range like ~ [1, 10] for visual representation, does not affect results
from louter.util.debug import trace

MULTIPLIER = 1000
PATH_TO_DATA = Path(__file__).parent.parent / 'data'

# inward_rolls = set(combinations('prmi', 3)) | set(combinations('PRMI', 3)) | set(combinations('prmi', 2)) | set(combinations('PRMI', 2))
inward_rolls = {'rmi', 'prm', 'pri', 'pi', 'pr', 'rm', 'ri', 'mi', 'px'}
inward_rolls |= set(map(str.upper, inward_rolls))
outward_rolls = set(map(lambda x: x[::-1], inward_rolls))
# inward_rolls = set(combinations('prmit', 3)) | set(combinations('PRMIT', 3)) | set(combinations('prmit', 2)) | set(combinations('PRMIT', 2))
# outward_rolls = set(combinations('timrp', 3)) | set(combinations('TIMRP', 3)) | set(combinations('timrp', 2)) | set(combinations('TIMRP', 2))
# outward_rolls = set(combinations('imrp', 3)) | set(combinations('IMRP', 3)) | set(combinations('imrp', 2)) | set(combinations('IMRP', 2))
same_finger_penalty = {k: p for k, p in zip("prmitxPRMITX", [7, 8, 5, 4, 5, 7] * 2)}
left_hand = "prmitx"


class Criterion:
    debug = False

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
         
        return result * 1.5

    def gram2_badness(self, keycaps):
        result = 0
        if self.debug:
            all_bigrams = set()
        for gram, freq in self.freqs2.items(): 
            fingers = keycaps.fingers[gram[0]], keycaps.fingers[gram[1]]
            # if fingers[0] == fingers[1]:
            #     multiplier = same_finger_penalty[fingers[0]] # * (keycaps.strain[gram[0]] + keycaps.strain[gram[1]])
            # el
            if fingers in inward_rolls:
                multiplier = 0.5
            elif fingers in outward_rolls:
                multiplier = 0.8
            elif (fingers[0] in left_hand) != (fingers[1] in left_hand):
                multiplier = 0.7
            else:
                multiplier = 1
            if fingers[0].islower() == fingers[1].islower():
                power = 2
                row_diff = abs(keycaps.rows[gram[0]] - keycaps.rows[gram[1]])
                if keycaps.rows[gram[0]] - keycaps.rows[gram[1]] == -1:
                    row_diff /= 4
                if keycaps.rows[gram[0]] - keycaps.rows[gram[1]] == 1:
                    row_diff /= 2
                if fingers[0] == fingers[1]:
                    same_finger = same_finger_penalty[fingers[0]] 
                elif fingers[0].lower() == 'x' and fingers[1].lower() != 'p':
                    same_finger = same_finger_penalty[fingers[1]]
                elif fingers[1].lower() == 'x' and fingers[0].lower() != 'p':
                    same_finger = same_finger_penalty[fingers[0]]
                else:
                    same_finger = 0 
                if gram[0] == gram[1]:
                    same_finger /= 5
                weak = (((fingers[0] in 'rpRP') + (fingers[1] in 'rpRP')) ** 2) / 4 + 1
                multiplier *= (row_diff * weak + 1 + same_finger) ** power


            strain = keycaps.strain[gram[0]] + keycaps.strain[gram[1]] 
            strain *= freq * multiplier
            result += strain

            if self.debug:
                all_bigrams.add((strain, gram))

        if self.debug:
            print(f"Most Damaging Bigrams ({self.__class__.__name__})")
            print("\n".join(map(str, sorted(all_bigrams, reverse=True)[:5])))
         
        return result

    def gram3_badness(self, keycaps):
        result = 0
        count = 0
        for gram, freq in self.freqs3.items():
            count += 1
            fingers = keycaps.fingers[gram[0]], keycaps.fingers[gram[1]], keycaps.fingers[gram[2]]
            multiplier = 1
            # if fingers[0] == fingers[1]:
            #     multiplier *= same_finger_penalty[fingers[1]]
            # if fingers[1] == fingers[2]:
            #     multiplier *= same_finger_penalty[fingers[1]]
            # if fingers[0] == fingers[1] == fingers[2]:
            #     multiplier *= same_finger_penalty[fingers[0]]
            # el
            if fingers in inward_rolls:
                multiplier *= 0.5
            elif fingers in outward_rolls:
                multiplier *= 0.8
            if fingers[0].islower() != fingers[1].islower() != fingers[2].islower():
                multiplier *= 0.7
            # else:
            #     if (fingers[0] in left_hand) != (fingers[1] in left_hand):
            #         multiplier *= 0.9
            #     if (fingers[1] in left_hand) != (fingers[2] in left_hand):
            #         multiplier *= 0.9
            strain = keycaps.strain[gram[0]] + keycaps.strain[gram[1]] + keycaps.strain[gram[2]]
            strain *= freq * multiplier
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


class HomePosition(Criterion):

    def __init__(self, valid_chars):
        self.zones = defaultdict(lambda: 3)
        self.zones.update({k:1 for k in "AEIOSTNR"})
        self.zones.update({k:2 for k in "KULD"})
        self.zones['◆'] = 5

    def __call__(self, keycaps):
        if keycaps.badness.get(self.__class__.__qualname__) is None: 
            keycaps.badness[self.__class__.__qualname__] = self.calc(keycaps) 
        return keycaps.badness[self.__class__.__qualname__]

    def calc(self, keycaps):
        result = 10
        for k, z in keycaps.zones.items():
            result += max(0, z - self.zones[k])
        return result


class HandBalanceEN(Criterion):
    freqs = None

    def __init__(self, valid_chars) -> None:
        if not HandBalanceEN.freqs:
            freqs = {}
            for line in open(PATH_TO_DATA / 'en' / '1grams.txt'):
                gram, freq = line.split()
                if all(l in valid_chars for l in gram):
                    freqs[gram] = float(freq)
            HandBalanceEN.freqs = freqs

    def __call__(self, keycaps):
        if keycaps.badness.get(self.__class__.__qualname__) is None: 
            keycaps.badness[self.__class__.__qualname__] = self.hand_balance_badness(keycaps) 
        return keycaps.badness[self.__class__.__qualname__]

    def hand_balance_badness(self, keycaps):
        counter = Counter()
        for gram, freq in self.freqs.items():
            counter[keycaps.fingers[gram] in left_hand] += freq
        # counter[keycaps.fingers[SPACE] in "primt"] += 0.02
        badness = counter[True] / counter[False]
        if badness < 1:
            badness = 1 / badness
            badness *= 1.1
        badness *= 10
        return badness


class HandBalanceLT(Criterion):
    freqs = None

    def __init__(self, valid_chars) -> None:
        if not HandBalanceLT.freqs:
            freqs = {}
            for line in open(PATH_TO_DATA / 'lt' / '1grams.txt'):
                gram, freq = line.split()
                if all(l in valid_chars for l in gram):
                    freqs[gram] = float(freq)
            HandBalanceLT.freqs = freqs

    def __call__(self, keycaps):
        if keycaps.badness.get(self.__class__.__qualname__) is None: 
            keycaps.badness[self.__class__.__qualname__] = self.hand_balance_badness(keycaps) 
        return keycaps.badness[self.__class__.__qualname__]

    def hand_balance_badness(self, keycaps):
        counter = Counter()
        for gram, freq in self.freqs.items():
            try:
                counter[keycaps.fingers[gram] in left_hand] += freq
            except KeyError:
                print(keycaps.fingers)
                raise
        # counter[keycaps.fingers[SPACE] in "primt"] += 0.02
        badness = counter[True] / counter[False]
        if badness < 1:
            badness = 1 / badness
            badness *= 1.1
        badness *= 10
        return badness



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
            result += f"{criterion!s:>15}: {criterion(self.keycaps):12.4f}"
            result += '\n'
        result += f"{'TOTAL':>15}: {self():12.4f}"
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


pauleikis_criteria = partial(Criteria, HandBalanceLT, LT, HandBalanceEN, EN, HomePosition, powers=[1.8, 2, 1.8, 2, 2])
# pauleikis_criteria = partial(Criteria, HandBalanceLT, LT, HandBalanceEN, EN, powers=[1.1, 2.2, 1.1, 2])
english_criteria = partial(Criteria, EN)


if __name__ == '__main__':
    from louter.core.keyboard import Ergodox, ANSI, Cradox
    from louter.core.keycaps import cool_classidox, cool_planck
    Criterion.debug = True
    import sys
    if len(sys.argv) > 1:
        print(pauleikis_criteria(keycaps=cool_planck(sys.argv[1])))
        exit(0)

    a = cool_planck("◆CMKB  JOHF◆◆UNTSWQREIA◆◆GVPD  LZYX◆◆◆◆◆◆◆◆◆◆◆◆")
    b = cool_planck("◆CMKB  JOHF◆"[::-1] + "◆UNTSWQREIA◆"[::-1] + "◆GVPD  LZYX◆"[::-1] + "◆◆◆◆◆◆◆◆◆◆◆")
    # c = cool_planck("◆WMKPBZHOYX◆◆UNTSFJREIA◆◆CVGD  LQ  ◆◆◆◆◆◆◆◆◆◆◆◆")
    # b = cool_classidox("◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ČJMBĘ◆DPĖŪ◆◆◆ŽKLTAFVSEIOĄ◆◆◆WCGHĮQRŠYŲ◆◆◆◆◆◆◆◆◆ZX◆◆◆◆◆◆◆UN◆◆◆")
    # c = KeyCaps("◆◆◆ŪĘ ◆◆ŲŽČ◆◆◆◆◆QOYĄXMLZ◆◆◆◆◆ŠGAIĖBSRDJ◆◆◆◆HCFEĮWNVPK◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆U◆◆T◆◆", Madox)
    # c = KeyCaps("◆◆QĄĘ◆◆◆◆ČŠX◆◆◆ŪBOGŲWPLJZ◆◆◆◆HDIAĖFTSMK◆◆◆◆Y◆ĮECVNŽ◆◆◆◆◆◆◆◆◆◆◆UR◆◆◆◆◆◆◆◆◆◆◆◆", Ergodox)


    # z = KeyCaps("◆◆QŲŪ◆◆◆◆ĖXW◆◆◆ĮRGKŠĘDNYŽ◆◆◆ZJISMĄBOLHCČ◆◆◆F◆◆AVPU◆◆◆◆◆◆◆◆◆◆◆◆TE◆◆◆◆◆◆◆◆◆◆◆◆", Ergodox)
    print(pauleikis_criteria(keycaps=a))
    print(pauleikis_criteria(keycaps=b))
    # print(pauleikis_criteria(keycaps=c))
    # print(pauleikis_criteria(keycaps=c))
    # print(pauleikis_criteria(keycaps=c))

    # print(pauleikis_criteria(keycaps=generate_new_preferred_madox()))

