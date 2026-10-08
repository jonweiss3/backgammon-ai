from src.board import Board, WHITE, BLACK
from src.moves import Move, legal_moves_for_die


def test_white_moves_toward_lower_points():
    board = Board()
    board.points[10] = 1

    moves = legal_moves_for_die(board, WHITE, 3)

    assert Move(source=10, destination=7, die=3) in moves


def test_black_moves_toward_higher_points():
    board = Board()
    board.points[10] = -1

    moves = legal_moves_for_die(board, BLACK, 3)

    assert Move(source=10, destination=13, die=3) in moves


def test_cannot_move_to_blocked_point():
    board = Board()
    board.points[10] = 1
    board.points[7] = -2

    moves = legal_moves_for_die(board, WHITE, 3)

    assert moves == []


def test_can_hit_single_opposing_checker():
    board = Board()
    board.points[10] = 1
    board.points[7] = -1

    moves = legal_moves_for_die(board, WHITE, 3)

    assert moves == [
        Move(source=10, destination=7, die=3, hit=True)
    ]