"""
fingers:
pinky, ring, middle, index, thumb
"""
p, r, m, i, t, T, I, M, R, P = tuple("prmitTIMRP")


class PhysicalKeyboard:
    template = None
    keycaps = None
    size = 0

    strain = []
    fingers = []

    def __str__(self):
        return self.__class__.__name__ + '\n' + self.template.format(*[' '] * self.size)

    def __eq__(self, other):
        return type(self) is type(other)


class ANSI(PhysicalKeyboard):
    size = 47

    @property
    def template(self):
        return """\
┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│
└───┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬───┐
      │TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│
      └─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴───┘
        │TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│
        └─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┘
          │TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│
          └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
        """.replace('TTT', '{:^3}').strip()

    @property
    def strain(self):
        return [
            20,15,15, 9, 9,15,15,15,15, 9, 9,15,15,
                 7, 4, 3, 4, 8,15, 5, 3, 3,10,15,15,20,
                  2, 2, 1, 1, 5, 6, 1, 1, 2, 2, 5,
                  13,13, 4, 6,15, 4, 3,12,12, 8,
        ]

    @property
    def fingers(self):
        return [
            p, p, p, r, m, i, i, I, M, M, R, P, P,
                p, r, m, i, i, I, I, M, R, P, P, P, P,
                 p, r, m, i, i, I, I, M, R, P, P,
                  p, r, m, i, i, I, I, M, R, P,
        ]


class ISO(PhysicalKeyboard):
    size = 47

    @property
    def template(self):
        return """\
┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│
└───┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┐
      │TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│
      └─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┘
        │TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│
      ┌─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┘
      │TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│TTT│
      └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
        """.replace('TTT', '{:^3}').strip()

    @property
    def strain(self):
        return [
            20,15,15, 9, 9,15,15,15,15, 9, 9,15,15,
                 7, 4, 3, 4, 8,15, 5, 3, 3,10,15,15,
                  2, 2, 1, 1, 5, 6, 1, 1, 2, 2, 5,
                4,13,13, 4, 6,15, 4, 3,12,12, 8,
        ]

    @property
    def fingers(self):
        return [
            p, p, p, r, m, i, i, I, M, M, R, P, P,
                p, r, m, i, i, I, I, M, R, P, P, P,
                 p, r, m, i, i, I, I, M, R, P, P,
               p, p, r, m, i, i, I, I, M, R, P,
        ]


class Ergodox(PhysicalKeyboard):
    size = 76

    @property
    def template(self):
        return """\
┌────┬───┬───┬───┬───┬───┬───┐                    ┌───┬───┬───┬───┬───┬───┬────┐
│ TTT│TTT│TTT│TTT│TTT│TTT│TTT│                    │TTT│TTT│TTT│TTT│TTT│TTT│ TTT│
├────┼───┼───┼───┼───┼───┼───┤                    ├───┼───┼───┼───┼───┼───┼────┤
│ TTT│TTT│TTT│TTT│TTT│TTT│   │                    │   │TTT│TTT│TTT│TTT│TTT│ TTT│
├────┼───┼───┼───┼───┼───┤TTT│                    │TTT├───┼───┼───┼───┼───┼────┤
│ TTT│TTT│TTT│TTT│TTT│TTT├───┤                    ├───┤TTT│TTT│TTT│TTT│TTT│ TTT│
├────┼───┼───┼───┼───┼───┤TTT│                    │TTT├───┼───┼───┼───┼───┼────┤
│ TTT│TTT│TTT│TTT│TTT│TTT│   │┌───┬───┐  ┌───┬───┐│   │TTT│TTT│TTT│TTT│TTT│ TTT│
└┬───┼───┼───┼───┼───┼───┴───┘│TTT│TTT│  │TTT│TTT│└───┴───┼───┼───┼───┼───┼───┬┘
 │TTT│TTT│TTT│TTT│TTT│    ┌───┼───┼───┤  ├───┼───┼───┐    │TTT│TTT│TTT│TTT│TTT│
 └───┴───┴───┴───┴───┘    │   │   │TTT│  │TTT│   │   │    └───┴───┴───┴───┴───┘
                          │TTT│TTT├───┤  ├───┤TTT│TTT│
                          │   │   │TTT│  │TTT│   │   │
                          └───┴───┴───┘  └───┴───┴───┘   
            """.replace('TTT', '{:^3}').strip()

    @property
    def strain(self):
        return [
          5.2, 5, 5, 4, 5, 5,20,            20, 5, 5, 4, 5, 5, 5.2,
          5.1, 3, 2, 1, 2, 5,                   5, 2, 1, 2, 3, 5.1,
                             10,            10,
            5, 1, 1, 1, 1, 3,                   3, 1, 1, 1, 1, 5,
                             12,            12,
          5.1, 2, 4, 3, 1, 1,                   1, 1, 3, 4, 2, 5.1,
                                4, 7,   7, 4,
             7, 6, 5, 3, 1,                       1, 3, 5, 6, 7,
                                   9,   9,
                            1, 2,          2, 1,
                                   3,   3,
        ]

    @property
    def fingers(self):
        return [
            p, r, r, m, i, i, i,             I, I, I, M, R, R, P,
            p, p, r, m, i, i,                   I, I, M, R, P, P,
                              i,             I,
            p, p, r, m, i, i,                   I, I, M, R, P, P,
                              i,             I,
            p, p, r, m, i, t,                   T, I, M, R, P, P,
                                t, t,   T, T,
             p, p, r, t, t,                       T, T, R, P, P,
                                   t,   T,
                            t, t,          T, T,
                                   t,   T,
        ]


if __name__ == '__main__':
    print(ANSI())
    print(ISO())
    print(Ergodox())
