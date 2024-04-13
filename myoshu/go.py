from enum import Enum, IntEnum, auto


class GameError(Exception):
    pass


class Boardsize(IntEnum):
    NINE = 9
    THIRTEEN = 13
    NINETEEN = 19


class Colour(Enum):
    BLACK = auto()
    WHITE = auto()


HANDICAP_PLACEMENT: dict[Boardsize, list[int]] = {
    Boardsize.NINE: [25, 57, 61, 21, 41],
    Boardsize.THIRTEEN: [49, 121, 127, 43, 85, 82, 88, 46, 124],
    Boardsize.NINETEEN: [73, 289, 301, 61, 181, 175, 187, 67, 295],
}


class Stone:
    def __init__(self, pos: int, colour: Colour) -> None:
        self._pos = pos
        self._colour = colour


class Goban:
    def __init__(self, size: Boardsize, handicap: int = 0) -> None:
        self._size = size
        self._handicap = handicap
        self._groups: list[Group] = []
        if handicap > 5 and size == Boardsize.NINE:
            self._handicap = 5
            print("Handicaps for 9x9 boards limited to 5.")
        elif handicap > 9:
            self._handicap = 9
            print("Handicaps for 13x13 and 19x19 boards limited to 9.")
        self.place_handicap_stones()

    def place_handicap_stones(self) -> None:
        match self._handicap:
            case 0 | 1:
                return
            case 2 | 3 | 4 | 5 | 7 | 9:
                points = list(range(self._handicap))
            case 6:
                points = [0, 1, 2, 3, 5, 6]
            case 8:
                points = [0, 1, 2, 3, 5, 6, 7, 8]
            case _:
                assert False, "unreachable"
        for i in points:
            self._groups.append(
                Group(Stone(HANDICAP_PLACEMENT[self._size][i], Colour.BLACK))
            )


class Group:
    def __init__(self, stone: Stone) -> None:
        self._stones = [stone]


class Game:
    def __init__(self, size: int, p1_name: str, p2_name: str, handicap: int) -> None:
        self.p1_name = p1_name
        self.p2_name = p2_name
        self._board = Goban(Boardsize(size), handicap)
        self._next_player = Colour.WHITE if handicap > 1 else Colour.BLACK
        self._komi = 7.5 if handicap == 0 else 0.5

    @property
    def board(self) -> Goban:
        return self._board

    @board.setter
    def board(self, value: Goban) -> None:
        if not self._board:
            self._board = value
        else:
            raise GameError("Cannot replace the board associated with a game.")
