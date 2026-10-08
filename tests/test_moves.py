from src.board import Board, WHITE, BLACK
from src.moves import (
    Move,
    apply_move,
    legal_moves_for_die,
    legal_move_sequences,
)


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


def test_apply_move_does_not_change_original_board():
    board = Board()
    board.points[10] = 1

    move = Move(source=10, destination=7, die=3)
    new_board = apply_move(board, WHITE, move)

    assert board.points[10] == 1
    assert board.points[7] == 0

    assert new_board.points[10] == 0
    assert new_board.points[7] == 1


def test_hit_sends_opponent_to_bar():
    board = Board()
    board.points[10] = 1
    board.points[7] = -1

    move = Move(
        source=10,
        destination=7,
        die=3,
        hit=True,
    )

    new_board = apply_move(board, WHITE, move)

    assert new_board.points[7] == 1
    assert new_board.bar[BLACK] == 1


def test_checker_on_bar_must_enter_first():
    board = Board()
    board.bar[WHITE] = 1
    board.points[10] = 1

    moves = legal_moves_for_die(board, WHITE, 3)

    assert moves == [
        Move(
            source=None,
            destination=21,
            die=3,
        )
    ]


def test_blocked_bar_entry_gives_no_move_for_die():
    board = Board()
    board.bar[WHITE] = 1
    board.points[21] = -2

    moves = legal_moves_for_die(board, WHITE, 3)

    assert moves == []


def test_bar_entry_can_hit_blot():
    board = Board()
    board.bar[WHITE] = 1
    board.points[21] = -1

    moves = legal_moves_for_die(board, WHITE, 3)

    assert moves == [
        Move(
            source=None,
            destination=21,
            die=3,
            hit=True,
        )
    ]


def test_white_can_bear_off_with_exact_die():
    board = Board()
    board.points[2] = 1

    moves = legal_moves_for_die(board, WHITE, 3)

    assert Move(
        source=2,
        destination=None,
        die=3,
    ) in moves


def test_white_can_bear_off_with_oversized_die():
    board = Board()
    board.points[2] = 1

    moves = legal_moves_for_die(board, WHITE, 5)

    assert Move(
        source=2,
        destination=None,
        die=5,
    ) in moves


def test_cannot_oversize_bear_off_if_checker_is_farther_back():
    board = Board()
    board.points[2] = 1
    board.points[4] = 1

    moves = legal_moves_for_die(board, WHITE, 5)

    assert Move(
        source=2,
        destination=None,
        die=5,
    ) not in moves


def test_black_can_bear_off_with_exact_die():
    board = Board()
    board.points[21] = -1

    moves = legal_moves_for_die(board, BLACK, 3)

    assert Move(
        source=21,
        destination=None,
        die=3,
    ) in moves


def test_apply_bear_off_increases_off_count():
    board = Board()
    board.points[2] = 1

    move = Move(
        source=2,
        destination=None,
        die=3,
    )

    new_board = apply_move(board, WHITE, move)

    assert new_board.points[2] == 0
    assert new_board.off[WHITE] == 1


def test_turn_uses_both_dice_when_possible():
    board = Board()
    board.points[10] = 1

    sequences = legal_move_sequences(
        board,
        WHITE,
        (2, 3),
    )

    assert sequences
    assert all(len(sequence) == 2 for sequence in sequences)


def test_higher_die_must_be_used_if_only_one_can_be_played():
    board = Board()
    board.points[5] = 1

    # Both first moves are possible, but either move then encounters
    # the blocked point at index 2.
    board.points[2] = -2

    sequences = legal_move_sequences(
        board,
        WHITE,
        (1, 2),
    )

    assert sequences
    assert all(len(sequence) == 1 for sequence in sequences)
    assert all(sequence[0].die == 2 for sequence in sequences)


def test_doubles_allow_four_moves():
    board = Board()
    board.points[10] = 1

    sequences = legal_move_sequences(
        board,
        WHITE,
        (1, 1),
    )

    assert sequences
    assert all(len(sequence) == 4 for sequence in sequences)