import random
from functools import partial
from typing import Union, Type

from louter.core.keyboard import ISO, ANSI, PhysicalKeyboard, Ergodox

RESERVED = '◆'
invalid_sources = (None, ' ', RESERVED)
invalid_targets = (RESERVED,)
finger_adj = {k: p for k, p in zip("prmitPRMIT", [1.2, 1, 0.9, 0.8, 0.9] * 2)}


class KeyCaps:

    def __init__(self, keycaps, keyboard: Union[Type[PhysicalKeyboard], PhysicalKeyboard], name=None):
        self.keycaps = tuple(k.upper() if k else k for k in keycaps)

        if type(keyboard) is type:
            keyboard = keyboard()
        self.keyboard = keyboard
        self.name = name
        self.fingers = {k: f for k, f in zip(self.keycaps, self.keyboard.fingers)}
        self.strain = {k: s * finger_adj[f] for k, s, f in zip(self.keycaps, self.keyboard.strain, self.keyboard.fingers)}
        self.fitness = {}

        assert len(self.keycaps) == self.keyboard.size, f"{len(self.keycaps)} != {self.keyboard.size}"
        assert not self.has_duplicates()

    def has_duplicates(self):
        unique_letters = set(self.keycaps) - {' ', None, RESERVED}
        total_letters = sum(k not in {' ', None, RESERVED} for k in self.keycaps)
        return bool(total_letters - len(unique_letters))

    def reordered(self, keycaps):
        return KeyCaps(keycaps, self.keyboard)

    def mutated(self):
        source_idx = random.choice([idx for idx, key in enumerate(self.keycaps) if key not in invalid_sources])
        target_idx = random.choice([idx for idx, key in enumerate(self.keycaps) if key not in invalid_targets and idx != source_idx])
        keycaps = list(self.keycaps)
        keycaps[target_idx], keycaps[source_idx] = keycaps[source_idx], keycaps[target_idx]
        return self.reordered(keycaps)

    def __call__(self):
        return self.reordered(self.keycaps)

    def __matmul__(self, other):
        assert isinstance(other, KeyCaps)
        assert self.keyboard == other.keyboard
        other = other.keycaps
        keycaps = self.keycaps
        new = [a if a == b else None for a, b in zip(keycaps, other)]
        missing = set(keycaps) - set(new) - {' ', None, RESERVED}
        missing_idx = {idx for idx, key in enumerate(new) if key is None}
        still_missing = set()
        while missing:
            letter = random.sample(missing, 1)[0]
            missing.discard(letter)
            for l in random.sample((keycaps, other), 2):
                idx = l.index(letter)
                if new[idx] is None:
                    new[idx] = letter
                    missing_idx.discard(idx)
                    break
            else:
                still_missing.add(letter)
        while still_missing:
            letter = random.sample(still_missing, 1)[0]
            still_missing.discard(letter)
            idx = random.sample(missing_idx, 1)[0]
            missing_idx.discard(idx)
            new[idx] = letter
        return self.reordered(new)

    def __rshift__(self, other):
        result = self
        for _ in range(other):
            result = result.mutated()
        return result

    def __str__(self):
        result = ''
        if self.name:
            result += self.name + '\n'
        result += self.keyboard.template.format(*[x if x else ' ' for x in self.keycaps])
        return result

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        assert self.keyboard == other.keyboard
        assert self.name == other.name
        assert self.fingers == other.fingers
        assert self.strain == other.strain
        return self.keycaps == other.keycaps

    def __hash__(self):
        return hash(self.keycaps)


class RandomKeyCaps(KeyCaps):

    def __init__(self, keycaps, keyboard: Union[Type[PhysicalKeyboard], PhysicalKeyboard], name=None):
        keycaps = list(keycaps)
        if RESERVED in keycaps:
            assert len(keycaps) == keyboard.size
            unfrozen_indices, unfrozen_subset = zip(*[(i, e) for i, e in enumerate(keycaps) if e != RESERVED])
            unfrozen_indices = list(unfrozen_indices)
            random.shuffle(unfrozen_indices)
            for i, e in zip(unfrozen_indices, unfrozen_subset):
                keycaps[i] = e
        elif len(keycaps) < keyboard.size:
            keycaps += [None] * (keyboard.size - len(keycaps))
            keycaps = random.sample(keycaps, len(keycaps))
        super().__init__(keycaps, keyboard, name)


iso_with_lt = KeyCaps(" ĄČĘĖĮŠŲŪ   ŽQWERTYUIOP  ASDFGHJKL   ZXCVBNM   ", ISO, 'ISO QWERTY with LT')
ansi_with_lt = KeyCaps(" ĄČĘĖĮŠŲŪ   ŽQWERTYUIOP   ASDFGHJKL  ZXCVBNM   ", ANSI, 'ANSI QWERTY with LT')
ansi_dvorak = KeyCaps(" ĄČĘĖĮŠŲŪ   Ž   PYFGCRL   AOEUIDHTNS  QJKXBMWVZ", ANSI, 'ANSI DVORAK with LT')
ansi_colemak = KeyCaps(" ĄČĘĖĮŠŲŪ   ŽQWFPGJLUY    ARSTDHNEIO ZXCVBKM   ", ANSI, 'ANSI COLEMAK with LT')
ansi_workman = KeyCaps(" ĄČĘĖĮŠŲŪ   ŽQDRWBJFUP    ASHTGYNEOI ZXMCVKL   ", ANSI, 'ANSI WORKMAN with LT')

ergodox = KeyCaps("=ĄČĘĖĮ  ŠŲŪŽ:\""
                                  " QWERTYUIOP/"
                                  "  "
                                  "_ASDFGHJKL,."
                                  "  "
                                  "Z◆XCVBNM[]{}"
                                  "◆◆◆◆"
                                  "◆◆◆◆◆◆◆()|"
                                  "◆◆"
                                  "◆◆◆◆"
                                  "◆◆"
                                , Ergodox, 'Ergodox'
                                )
generate_new_random_ergodox = partial(
    RandomKeyCaps,
    " ĄČĘĖĮ  ŠŲŪŽ  "
    " QWERTYUIOP "
    "  "
    " ASDFGHJKL  "
    "  "
    "Z◆XCVBNM    "
    "◆◆◆◆"
    "◆◆◆       "
    "◆◆"
    "◆◆◆◆"
    "◆◆",
    Ergodox,
)


if __name__ == '__main__':
    # print(iso_with_lt)
    # print(ansi_with_lt)
    # print(ansi_dvorak)
    # print(ansi_workman)
    # print(ansi_colemak)

    # print(generate_new_random_ergodox())

    # print(KeyCaps(map(str, Ergodox().strain), Ergodox))
    # print(len("ĄČĘĖĮŠŲŪŽQWERTYUIOPASDFGHJKLZXCVBNM.,_=\"/:()[]|{}"))


    generate_new_random_ergodox = partial(
        RandomKeyCaps,
        "           A  "
        "            "
        "  "
        "            "
        "  "
        "            "
        "◆◆◆◆"
        "◆◆◆       "
        "◆◆"
        "◆◆◆◆"
        "◆◆",
        Ergodox,
    )
    dox = generate_new_random_ergodox()
    print(dox)
    print(dox >> 1)
    print(dox >> 1)
    print(dox >> 1)
