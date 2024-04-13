class GameError(Exception):
    pass


class Goban:
    def __init__(self, size: int, handicap: int = 0) -> None:
        self._size = size
        self._handicap = handicap


class Game:
    def __init__(
        self, boardsize: int, p1_name: str, p2_name: str, handicap: int
    ) -> None:
        self.p1_name = p1_name
        self.p2_name = p2_name
        self._board = Goban(boardsize, handicap)

    @property
    def board(self) -> Goban:
        return self._board

    @board.setter
    def board(self, value: Goban) -> None:
        if not self._board:
            self._board = value
        else:
            raise GameError("Cannot replace the board associated with a game.")
