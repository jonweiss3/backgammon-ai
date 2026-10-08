from src.board import Board, WHITE, BLACK


def test_starting_position_has_15_checkers_each():
    board = Board.starting_position()

    assert board.total_checkers(WHITE) == 15
    assert board.total_checkers(BLACK) == 15


def test_starting_position():
    board = Board.starting_position()

    assert board.points[23] == 2
    assert board.points[12] == 5
    assert board.points[7] == 3
    assert board.points[5] == 5

    assert board.points[0] == -2
    assert board.points[11] == -5
    assert board.points[16] == -3
    assert board.points[18] == -5