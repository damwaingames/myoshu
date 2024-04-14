from typing import Generator

import pytest

import myoshu.go as go


class TestGame:
    def test_creating_game_initializes_board(self, default_game) -> None:
        assert default_game.board._size == 19
        assert default_game.p1_name == "Black player"
        assert default_game.p2_name == "White player"
        assert default_game.board._handicap == 0
        assert default_game._next_player == go.Colour.BLACK
        assert default_game._komi == 7.5

    def test_cannot_replace_game_board(self, default_game) -> None:
        with pytest.raises(go.GameError):
            default_game.board = go.Goban(go.Boardsize(9), 4)

    def test_handicap_game_setup(self, handicap_full_game) -> None:
        current_handicap = handicap_full_game._board._handicap
        assert handicap_full_game._komi == 0.5
        if current_handicap > 1:
            assert len(handicap_full_game._board._groups) == current_handicap
            assert handicap_full_game._next_player == go.Colour.WHITE
        else:
            assert handicap_full_game._next_player == go.Colour.BLACK


@pytest.fixture
def default_game() -> go.Game:
    return go.Game(19, "Black player", "White player", 0)


@pytest.fixture(params=[1, 2, 3, 4, 5, 6, 7, 8, 9])
def handicap_full_game(request) -> Generator[go.Game, None, None]:
    game = go.Game(19, "Black player", "White player", request.param)
    yield game
