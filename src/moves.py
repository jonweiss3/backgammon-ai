from dataclasses import dataclass

from src.board import Board, WHITE, BLACK


@dataclass(frozen=True)
class Move:
    source: int
    destination: int
    die: int
    hit: bool = False


def legal_moves_for_die(board: Board, player: int, die: int) -> list[Move]:
    moves = []

    direction = -1 if player == WHITE else 1

    for source, count in enumerate(board.points):
        # Skip points that do not contain this player's checkers.
        if count * player <= 0:
            continue

        destination = source + direction * die

        # Bearing off will be handled later.
        if destination < 0 or destination > 23:
            continue

        destination_count = board.points[destination]

        # A point with 2+ opposing checkers is blocked.
        if destination_count * player <= -2:
            continue

        hit = destination_count * player == -1

        moves.append(
            Move(
                source=source,
                destination=destination,
                die=die,
                hit=hit,
            )
        )

    return moves