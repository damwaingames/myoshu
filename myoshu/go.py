from __future__ import annotations

from enum import Enum, IntEnum, auto
from typing import assert_never


class GameError(Exception):
    pass


class IllegalPlacement(Exception):
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

KANJI_NUMBERS: list[str] = [
    "零",
    "一",
    "二",
    "三",
    "四",
    "五",
    "六",
    "七",
    "八",
    "九",
    "十",
    "十一",
    "十二",
    "十三",
    "十四",
    "十五",
    "十六",
    "十七",
    "十八",
    "十九",
]


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

    @property
    def black_groups(self) -> set["Group"]:
        return {group for group in self._groups if group._colour == Colour.BLACK}

    @property
    def white_groups(self) -> set["Group"]:
        return {group for group in self._groups if group._colour == Colour.WHITE}

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
                Group(HANDICAP_PLACEMENT[self._size][i], Colour.BLACK, self)
            )

    def find_stone(self, pos: int) -> "Stone" | None:
        for group in self._groups:
            for stone in group._stones:
                if stone._pos == pos:
                    return stone
        return None

    def find_stones(self, positions: set[int]) -> set["Stone"]:
        stones = set()
        for group in self._groups:
            for stone in group._stones:
                for pos in positions:
                    if stone._pos == pos:
                        stones.add(stone)
        return stones

    def find_stone_position(self, pos: int) -> int | None:
        for group in self._groups:
            for stone in group._stones:
                if stone._pos == pos:
                    return stone._pos
        return None

    def find_stones_positions(self, positions: set[int]) -> set[int]:
        output = set()
        for group in self._groups:
            for stone in group._stones:
                for pos in positions:
                    if stone._pos == pos:
                        output.add(pos)
        return output


class Stone:
    def __init__(self, pos: int, colour: Colour, group: "Group") -> None:
        self._pos = pos
        self._colour = colour
        self._group = group

    def __str__(self) -> str:
        return (
            self.convert_pos_to_coord()
            + ", "
            + str(self._colour)
            + " : "
            + str(self.neighbours())
        )

    def __repr__(self) -> str:
        return str(self)

    def neighbours(self) -> set[int]:
        adjacent = set()
        size = self._group._board._size
        if self._pos - size > 0:  # Up
            adjacent.add(self._pos - size)
        if self._pos + size <= size**2:  # Down
            adjacent.add(self._pos + size)
        if self._pos % size != 1:  # Left
            adjacent.add(self._pos - 1)
        if self._pos % size != 0:  # Right
            adjacent.add(self._pos + 1)
        return adjacent

    def convert_pos_to_coord(self) -> str:
        file = self._pos % self._group._board._size
        file = self._group._board._size if file == 0 else file
        rank = self._pos // self._group._board._size
        rank = rank if file == self._group._board._size else rank + 1
        return f"{file}-{rank}"

    def convert_pos_to_sgf(self) -> str:
        coord = self.convert_pos_to_coord()
        file, rank = coord.split("-")
        return chr(int(file) + 96) + chr(int(rank) + 96)


class Group:
    def __init__(self, pos: int, colour: Colour, board: Goban) -> None:
        self._stones = {Stone(pos, colour, self)}
        self._board = board
        self._colour = colour

    def __str__(self) -> str:
        return str(self._stones)

    def __repr__(self) -> str:
        return str(self)

    def liberties(self) -> set[int]:
        neighbours: set[int] = set()
        for stone in self._stones:
            neighbours = neighbours.union(stone.neighbours())
        neighbours = neighbours.difference(self._stones)
        return neighbours.difference(self._board.find_stones_positions(neighbours))


class Game:
    def __init__(self, size: int, p1_name: str, p2_name: str, handicap: int) -> None:
        self.p1_name = p1_name
        self.p2_name = p2_name
        self.current_move = 1
        self.moves: list[tuple[Colour, int]] = []
        self._board = Goban(Boardsize(size), handicap)
        self._next_player = Colour.WHITE if handicap > 1 else Colour.BLACK
        self._komi = 7.5 if handicap == 0 else 0.5

    @property
    def board(self) -> Goban:
        return self._board

    @property
    def current_player(self) -> Colour:
        return self._next_player

    def advance_turn(self) -> None:
        for group in self.board._groups:
            if len(group.liberties()) == 0:
                self.board._groups.remove(group)
        match self._next_player:
            case Colour.BLACK:
                self._next_player = Colour.WHITE
            case Colour.WHITE:
                self._next_player = Colour.BLACK
            case _:
                assert_never(self.current_player)
        self.current_move += 1

    def make_move(self, pos: int) -> None:
        if stone := self.board.find_stone(pos):
            raise IllegalPlacement(
                f"There is already a stone at {stone.convert_pos_to_coord()}"
            )
        match self._next_player:
            case Colour.BLACK:
                groups = self.board.black_groups
            case Colour.WHITE:
                groups = self.board.white_groups
            case _:
                assert_never(self._next_player)
        neighbouring_groups: set[Group] = set()
        for group in groups:
            if pos in group.liberties():
                neighbouring_groups.add(group)
        if neighbouring_groups:
            print(neighbouring_groups)
            new_group = Group(pos, self._next_player, self.board)
            for group in neighbouring_groups:
                for stone in group._stones:
                    new_group._stones.add(stone)
                self.board._groups.remove(group)
            self.board._groups.append(new_group)
            self.moves.append((self.current_player, pos))
            self.advance_turn()
        else:
            new_group = Group(pos, self._next_player, self.board)
            if len(new_group.liberties()) == 0:
                raise IllegalPlacement(
                    f"Placing a stone at {new_group._stones.pop().convert_pos_to_coord} would be a suicide move."
                )
            self.board._groups.append(new_group)
            self.moves.append((self.current_player, pos))
            self.advance_turn()
