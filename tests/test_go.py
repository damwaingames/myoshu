from typing import Generator

import pytest

import myoshu.go as go


class TestGame:
    def test_creating_game_initializes_board(self, default_full_game) -> None:
        assert default_full_game.board._size == 19
        assert default_full_game.p1_name == "Black player"
        assert default_full_game.p2_name == "White player"
        assert default_full_game.board._handicap == 0
        assert default_full_game._next_player == go.Colour.BLACK
        assert default_full_game._komi == 7.5

    def test_cannot_replace_game_board(self, default_full_game) -> None:
        with pytest.raises(go.GameError):
            default_full_game.board = go.Goban(go.Boardsize(9), 4)

    def test_handicap_full_game_setup(self, handicap_full_game) -> None:
        current_handicap = handicap_full_game._board._handicap
        assert current_handicap <= 9
        assert handicap_full_game._komi == 0.5
        if current_handicap > 1:
            assert len(handicap_full_game._board._groups) == current_handicap
            assert handicap_full_game._next_player == go.Colour.WHITE
        else:
            assert handicap_full_game._next_player == go.Colour.BLACK

    def test_handicap_nine_by_nine_setup(self, handicap_nine_by_nine_game) -> None:
        current_handicap = handicap_nine_by_nine_game._board._handicap
        assert current_handicap <= 5
        assert handicap_nine_by_nine_game._komi == 0.5
        if current_handicap > 1:
            assert len(handicap_nine_by_nine_game._board._groups) == current_handicap
            assert handicap_nine_by_nine_game._next_player == go.Colour.WHITE
        else:
            assert handicap_nine_by_nine_game._next_player == go.Colour.BLACK

    def test_convert_stone_pos_to_coordinates(self, default_full_game) -> None:
        one_one = go.Group(
            1, default_full_game._next_player, default_full_game._board
        )._stones[0]
        two_one = go.Group(
            2, default_full_game._next_player, default_full_game._board
        )._stones[0]
        nineteen_one = go.Group(
            19, default_full_game._next_player, default_full_game._board
        )._stones[0]
        one_two = go.Group(
            20, default_full_game._next_player, default_full_game._board
        )._stones[0]
        nineteen_two = go.Group(
            38, default_full_game._next_player, default_full_game._board
        )._stones[0]
        tengen = go.Group(
            181, default_full_game._next_player, default_full_game._board
        )._stones[0]
        one_nineteen = go.Group(
            343, default_full_game._next_player, default_full_game._board
        )._stones[0]
        nineteen_nineteen = go.Group(
            361, default_full_game._next_player, default_full_game._board
        )._stones[0]
        assert one_one.convert_pos_to_coord() == "1-1"
        assert one_one.convert_pos_to_sgf() == "aa"
        assert two_one.convert_pos_to_coord() == "2-1"
        assert two_one.convert_pos_to_sgf() == "ba"
        assert nineteen_one.convert_pos_to_coord() == "19-1"
        assert nineteen_one.convert_pos_to_sgf() == "sa"
        assert one_two.convert_pos_to_coord() == "1-2"
        assert one_two.convert_pos_to_sgf() == "ab"
        assert nineteen_two.convert_pos_to_coord() == "19-2"
        assert nineteen_two.convert_pos_to_sgf() == "sb"
        assert tengen.convert_pos_to_coord() == "10-10"
        assert tengen.convert_pos_to_sgf() == "jj"
        assert one_nineteen.convert_pos_to_coord() == "1-19"
        assert one_nineteen.convert_pos_to_sgf() == "as"
        assert nineteen_nineteen.convert_pos_to_coord() == "19-19"
        assert nineteen_nineteen.convert_pos_to_sgf() == "ss"

    def test_stones_have_correct_neighbours(self, default_full_game) -> None:
        one_one = go.Group(
            1, default_full_game._next_player, default_full_game._board
        )._stones[0]
        two_one = go.Group(
            2, default_full_game._next_player, default_full_game._board
        )._stones[0]
        nineteen_one = go.Group(
            19, default_full_game._next_player, default_full_game._board
        )._stones[0]
        one_two = go.Group(
            20, default_full_game._next_player, default_full_game._board
        )._stones[0]
        nineteen_two = go.Group(
            38, default_full_game._next_player, default_full_game._board
        )._stones[0]
        tengen = go.Group(
            181, default_full_game._next_player, default_full_game._board
        )._stones[0]
        one_nineteen = go.Group(
            343, default_full_game._next_player, default_full_game._board
        )._stones[0]
        nineteen_nineteen = go.Group(
            361, default_full_game._next_player, default_full_game._board
        )._stones[0]
        assert one_one.neighbours() == {2, 20}
        assert two_one.neighbours() == {1, 3, 21}
        assert nineteen_one.neighbours() == {18, 38}
        assert one_two.neighbours() == {1, 21, 39}
        assert nineteen_two.neighbours() == {19, 37, 57}
        assert tengen.neighbours() == {162, 180, 182, 200}
        assert one_nineteen.neighbours() == {324, 344}
        assert nineteen_nineteen.neighbours() == {342, 360}


@pytest.fixture
def default_full_game() -> go.Game:
    return go.Game(19, "Black player", "White player", 0)


@pytest.fixture(params=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
def handicap_full_game(request) -> Generator[go.Game, None, None]:
    game = go.Game(19, "Black player", "White player", request.param)
    yield game


@pytest.fixture(params=[1, 2, 3, 4, 5, 6])
def handicap_nine_by_nine_game(request) -> Generator[go.Game, None, None]:
    game = go.Game(9, "Black player", "White player", request.param)
    yield game
