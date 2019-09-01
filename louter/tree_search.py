from louter.core.criteria import pauleikis_criteria
from louter.core.keyboard import Ergodox, Madox
from louter.core.keycaps import KeyCaps

FINAL = set()


def find_improved(layout):
    print("".join(k if k else ' ' for k in layout.keycaps.keycaps))
    result = set()
    for _ in range(1000):
        if not _ % 100:
            print(_)
        new = layout >> 1
        if new < layout:
            result.add(new)
    return sorted(result)[:5] if result else None


def main():
    initial = KeyCaps("◆◆◆ŪĘ ◆◆ŲŽČ◆◆◆◆◆ZOYĄWMLQ◆◆◆◆◆ŠGAIĖBSRDJ◆◆◆◆HCXEĮFNVPK◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆U◆◆T◆◆", Madox)
    initial = pauleikis_criteria(keycaps=initial)
    pool = [initial]
    while True:
        new = set()
        for kb in pool[:10]:
            new_list = find_improved(kb)
            if new_list:
                new |= set(new_list)
        if new:
            pool = sorted(new)
        else:
            for kb in pool:
                print(kb)
            break


if __name__ == '__main__':
    main()
