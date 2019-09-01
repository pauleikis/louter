import random
import string
from functools import partial
from typing import Union, Type

from louter.core.keyboard import ISO, ANSI, PhysicalKeyboard, Ergodox, Madox, Cradox, Classidox, Planck

# locked = set("VDBJLTAWKCGHXUMPSEIRFYONZ")
# locked = set("KLTAUNSEIOCGHRZWXDPM")
# locked = set("ARSTNEIUODLK")
locked = set()
RESERVED = '◆'
invalid_sources = {None, RESERVED}
invalid_sources |= set(locked)
invalid_targets = {RESERVED}
invalid_targets |= set(locked)


class KeyCaps:

    def __init__(self, keycaps, keyboard: Union[Type[PhysicalKeyboard], PhysicalKeyboard], name=None):
        self.keycaps = tuple(k.upper() if k and not k == ' ' else None for k in keycaps)

        if type(keyboard) is type:
            keyboard = keyboard()
        self.keyboard = keyboard
        self.name = name
        # self.fingers = {k: f for k, f in zip(self.keycaps, self.keyboard.fingers) if k not in invalid_sources}
        self.fingers = {k: f for k, f in zip(self.keycaps, self.keyboard.fingers)}
        # self.strain = {k: s * finger_adj[f] for k, s, f in zip(self.keycaps, self.keyboard.strain, self.keyboard.fingers) if k not in invalid_sources}
        self.strain = {k: s for k, s in zip(self.keycaps, self.keyboard.strain)}
        self.badness = {}
        self.rows = {k: int(s) for k, s in zip(self.keycaps, self.keyboard.rows)}
        self.zones = {k: s for k, s in zip(self.keycaps, self.keyboard.zones)}
        # self.stretch = {}
        # for (a, b), m in self.keyboard.stretch.items():
        #     if self.keycaps[a] and self.keycaps[b]:
        #         self.stretch[self.keycaps[a] + self.keycaps[b]] = m
        #         self.stretch[self.keycaps[b] + self.keycaps[a]] = m


        assert len(self.keycaps) == self.keyboard.size, f"{len(self.keycaps)} != {self.keyboard.size}"
        assert not self.has_duplicates(), self.has_duplicates()  

    def has_duplicates(self):
        unique_letters = set(self.keycaps) - invalid_sources
        total_letters = [k for k in self.keycaps if k not in invalid_sources]
        for letter in unique_letters:
            total_letters.remove(letter)
            
        return total_letters

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
        missing = set(keycaps) - set(new) - invalid_sources
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
        result += '\n'
        result += "\"" + "".join(k if k else ' ' for k in self.keycaps) + "\""
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
            unfrozen_indices, unfrozen_subset = zip(*[(i, e) for i, e in enumerate(keycaps) if e not in invalid_sources])
            unfrozen_indices = list(unfrozen_indices)
            random.shuffle(unfrozen_indices)
            for i, e in zip(unfrozen_indices, unfrozen_subset):
                keycaps[i] = e
        elif len(keycaps) < keyboard.size:
            keycaps += [None] * (keyboard.size - len(keycaps))
            keycaps = random.sample(keycaps, len(keycaps))
        super().__init__(keycaps, keyboard, name)


# iso_with_lt = KeyCaps(" ĄČĘĖĮŠŲŪ   ŽQWERTYUIOP  ASDFGHJKL   ZXCVBNM   ", ISO, 'ISO QWERTY with LT')
# ansi_with_lt = KeyCaps(" ĄČĘĖĮŠŲŪ   ŽQWERTYUIOP   ASDFGHJKL  ZXCVBNM   ", ANSI, 'ANSI QWERTY with LT')
# ansi_dvorak = KeyCaps(" ĄČĘĖĮŠŲŪ   Ž   PYFGCRL   AOEUIDHTNS  QJKXBMWVZ", ANSI, 'ANSI DVORAK with LT')
# ansi_colemak = KeyCaps(" ĄČĘĖĮŠŲŪ   ŽQWFPGJLUY    ARSTDHNEIO ZXCVBKM   ", ANSI, 'ANSI COLEMAK with LT')
# ansi_colemak_dh = KeyCaps("             QWFPBJLUY    ARSTGKNEIO ZXCDVMH   ", ANSI, 'ANSI COLEMAK with LT')
# ansi_workman = KeyCaps(" ĄČĘĖĮŠŲŪ   ŽQDRWBJFUP    ASHTGYNEOI ZXMCVKL   ", ANSI, 'ANSI WORKMAN with LT')

# generate_new_random_ansi_english = partial(RandomKeyCaps, "QWERTYUIOPASDFGHJKLZXCVBNM", ANSI)

# ergodox = KeyCaps("=ĄČĘĖĮ  ŠŲŪŽ:\""
#                                   " QWERTYUIOP/"
#                                   "  "
#                                   "_ASDFGHJKL,."
#                                   "  "
#                                   "Z◆XCVBNM[]{}"
#                                   "◆◆◆◆"
#                                   "◆◆◆◆◆◆◆()|"
#                                   "◆◆"
#                                   "◆◆◆◆"
#                                   "◆◆"
#                                 , Ergodox, 'Ergodox'
#                                 )
# generate_new_random_ergodox = partial(
#     RandomKeyCaps,
#     "◆◆ŪŽČ◆◆◆◆ŠŲĘ◆◆"
#     "◆QWERTYUIOP◆"
#     "◆◆"
#     "ASDFGHJKLĄZX"
#     "◆◆"
#     "◆M◆ CVBN ◆◆◆"
#     "◆◆◆◆"
#     "◆◆◆◆ĖĮ◆◆◆◆"
#     "◆◆"
#     "◆◆◆◆"
#     "◆◆",
#     Ergodox,
# )

# generate_new_preferred_ergodox = partial(KeyCaps, "◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆QBOGXJPLZ ◆◆◆◆HDIAWFTSMK◆◆◆◆Y◆◆ECVN◆◆◆◆◆◆◆◆◆◆◆◆UR◆◆◆◆◆◆◆◆◆◆◆◆", Ergodox)
# generate_new_preferred_ergodox = partial(KeyCaps, "◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ GOYXZPLFQ◆◆◆◆HDAIWJSRMK◆◆◆◆B◆◆ECVN◆◆◆◆◆◆◆◆◆◆◆◆UT◆◆◆◆◆◆◆◆◆◆◆◆", Ergodox)
# generate_new_preferred_ergodox = partial(KeyCaps, "◆◆XVŪ◆◆◆◆QŠŲ◆◆◆WBSKZČTELŽ◆◆◆◆HMDOPFAYUR◆◆◆◆J◆ĘĮCĄIĖ◆◆◆◆◆◆◆◆◆◆◆NG◆◆◆◆◆◆◆◆◆◆◆◆", Ergodox)
# generate_new_preferred_ergodox = partial(KeyCaps, "◆◆QŪĘ◆◆◆◆ZŠX◆◆◆ĮGLHŲWBMJČ◆◆◆◆PKEIĖFANRD◆◆◆◆C◆ĄOYVTŽ◆◆◆◆◆◆◆◆◆◆◆US◆◆◆◆◆◆◆◆◆◆◆◆", Ergodox)
# generate_new_preferred_ergodox = partial(KeyCaps, "◆◆ĘĄX◆◆◆◆ČŠQ◆◆◆ŪBOGŲWPLJZ◆◆◆◆HDAIĖFSRMK◆◆◆◆Y◆ĮECVNŽ◆ ◆◆◆◆◆◆◆◆◆UT◆◆◆◆◆◆◆◆◆◆◆◆", Ergodox)
# generate_new_preferred_ergodox = partial(KeyCaps, "◆◆ XĘ◆◆◆◆ŠZQ◆◆◆ŪGOCĄJPLVČ◆◆◆◆HKAIYFSRMD◆◆◆◆Ė◆ŲEĮWNŽ◆B◆◆◆◆◆◆◆◆◆UT◆◆◆◆◆◆◆◆◆◆◆◆", Ergodox)
# generate_new_preferred_ergodox = partial(KeyCaps, "◆◆ XĘ◆◆◆◆ZWQ◆◆◆ŪGOFĮŠPLVČ◆◆◆◆HKAIYBSRMD◆◆◆◆Ė◆ŲEĄCNŽ◆J◆◆◆◆◆◆◆◆◆UT◆◆◆◆◆◆◆◆◆◆◆◆", Ergodox)
# generate_new_preferred_madox =  partial(KeyCaps,       "◆◆◆ŪĮ◆◆◆ĘŠŽ◆◆◆◆◆ZOYĄWMLQ◆◆◆◆◆ČGAIĖBSRDJ◆◆◆◆HCXEŲFNVPK◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆U◆◆T◆◆", Madox)
# generate_new_random_madox = partial(RandomKeyCaps, "◆◆◆XĘČ◆◆QZW◆◆◆◆◆GOFĮŠPLŪ◆◆◆◆◆HKAIYBSRMD◆◆◆◆ĖCVEĄŲNŽ J◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆U◆◆T◆◆", Madox)
# generate_new_preferred_cradox = partial(KeyCaps, "◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ZOYĄWMLĮ◆◆◆◆◆ČGAIĖBSRDJ◆◆◆ŪHCXEŲFTVPKQ◆◆◆◆◆Ę◆◆ŠŽ◆◆ ◆◆◆◆UN◆◆◆", Cradox)
# generate_new_random_cradox = partial(RandomKeyCaps, "◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ZOYĄWMLĮ◆◆◆◆◆ČGAIĖBSRDJ◆◆◆ŪHCXEŲFTVPKQ◆◆◆◆◆Ę◆◆ŠŽ◆◆ ◆◆◆◆UN◆◆◆", Cradox)
generate_new_random_planck = partial(RandomKeyCaps, "ABCDEFGHIJKLMNOPQRSTUVWXYZ               ◆     ", Planck)

generate_new_random_planck = partial(RandomKeyCaps, "◆FHOJ  MKPC◆◆AIERQWSTNU◆◆XYZL  DGBV◆◆◆◆◆◆◆◆◆◆◆◆", Planck)

cool_cradox = partial(KeyCaps, keyboard=Cradox)
cool_classidox = partial(KeyCaps, keyboard=Classidox)
cool_planck = partial(KeyCaps, keyboard=Planck)

if __name__ == '__main__':
    # print(iso_with_lt)
    # print(ansi_with_lt)
    # print(ansi_dvorak)
    # print(ansi_workman)
    # print(ansi_colemak)
    # print(ansi_colemak_dh)
    print(generate_new_random_planck())
    # print(cool_classidox("◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ČJVBĄ◆MDYŪ◆◆◆QKLTAFŽSEIOĘ◆◆◆WCGHĮŠRPĖŲ◆◆◆◆◆◆◆◆◆ZX◆◆◆◆◆◆◆UN◆◆◆"))
    # print(cool_classidox("◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ČJPBĄ◆MDYŪ◆◆◆QKLTAFŽSEIOĘ◆◆◆WCGHĮŠRVĖŲ◆◆◆◆◆◆◆◆◆ZX◆◆◆◆◆◆◆UN◆◆◆"))