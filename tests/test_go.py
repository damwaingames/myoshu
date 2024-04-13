import pytest

import myoshu.go as go


class TestGame:
    test_game = go.Game(19, "Black player", "White player", 0)

    def test_creating_game_initializes_board(self) -> None:
        assert self.test_game.board._size == 19
        assert self.test_game.p1_name == "Black player"
        assert self.test_game.p2_name == "White player"
        assert self.test_game.board._handicap == 0

    def test_cannot_replace_game_board(self) -> None:
        with pytest.raises(go.GameError):
            self.test_game.board = go.Goban(9, 4)
