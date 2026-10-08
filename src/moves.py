from dataclasses import dataclass

from src.board import Board, WHITE, BLACK


@dataclass(frozen=True)
class Move:
    source: int | None
    destination: int | None
    die: int
    hit: bool = False

    @property
    def from_bar(self) -> bool:
        return self.source is None

    @property
    def bears_off(self) -> bool:
        return self.destination is None


def _validate_player(player: int) -> None:
    if player not in (WHITE, BLACK):
        raise ValueError("Player must be WHITE or BLACK.")


def _validate_die(die: int) -> None:
    if die < 1 or die > 6:
        raise ValueError("Die must be between 1 and 6.")


def _bar_destination(player: int, die: int) -> int:
    if player == WHITE:
        return 24 - die

    return die - 1


def _point_is_open(board: Board, player: int, destination: int) -> bool:
    return board.points[destination] * player >= -1


def _can_bear_off(
    board: Board,
    player: int,
    source: int,
    die: int,
) -> bool:
    if not board.all_in_home_board(player):
        return False

    if player == WHITE:
        distance_to_off = source + 1

        if die == distance_to_off:
            return True

        if die < distance_to_off:
            return False

        # An oversized die can only bear this checker off if there
        # are no checkers farther from the edge.
        return not any(
            board.points[index] * player > 0
            for index in range(source + 1, 6)
        )

    distance_to_off = 24 - source

    if die == distance_to_off:
        return True

    if die < distance_to_off:
        return False

    return not any(
        board.points[index] * player > 0
        for index in range(18, source)
    )


def legal_moves_for_die(
    board: Board,
    player: int,
    die: int,
) -> list[Move]:
    _validate_player(player)
    _validate_die(die)

    # A checker on the bar must re-enter before any other checker moves.
    if board.bar[player] > 0:
        destination = _bar_destination(player, die)

        if not _point_is_open(board, player, destination):
            return []

        return [
            Move(
                source=None,
                destination=destination,
                die=die,
                hit=board.points[destination] * player == -1,
            )
        ]

    moves = []
    direction = -1 if player == WHITE else 1

    for source, count in enumerate(board.points):
        if count * player <= 0:
            continue

        destination = source + direction * die

        if 0 <= destination <= 23:
            if not _point_is_open(board, player, destination):
                continue

            moves.append(
                Move(
                    source=source,
                    destination=destination,
                    die=die,
                    hit=board.points[destination] * player == -1,
                )
            )

        elif _can_bear_off(board, player, source, die):
            moves.append(
                Move(
                    source=source,
                    destination=None,
                    die=die,
                )
            )

    return moves


def apply_move(
    board: Board,
    player: int,
    move: Move,
) -> Board:
    _validate_player(player)

    new_board = board.copy()

    if move.source is None:
        if new_board.bar[player] <= 0:
            raise ValueError("Player has no checker on the bar.")

        new_board.bar[player] -= 1

    else:
        if new_board.points[move.source] * player <= 0:
            raise ValueError("Source does not contain player's checker.")

        new_board.points[move.source] -= player

    if move.destination is None:
        new_board.off[player] += 1
        return new_board

    destination_count = new_board.points[move.destination]

    if destination_count * player <= -2:
        raise ValueError("Destination is blocked.")

    # Hit a blot.
    if destination_count == -player:
        new_board.points[move.destination] = 0
        new_board.bar[-player] += 1

    new_board.points[move.destination] += player

    return new_board


def apply_sequence(
    board: Board,
    player: int,
    sequence: tuple[Move, ...],
) -> Board:
    result = board

    for move in sequence:
        result = apply_move(result, player, move)

    return result


def legal_move_sequences(
    board: Board,
    player: int,
    dice: tuple[int, int],
) -> list[tuple[Move, ...]]:
    _validate_player(player)

    die_one, die_two = dice
    _validate_die(die_one)
    _validate_die(die_two)

    if die_one == die_two:
        remaining_dice = (die_one,) * 4
    else:
        remaining_dice = dice

    sequences: list[tuple[Move, ...]] = []

    def search(
        position: Board,
        remaining: tuple[int, ...],
        sequence: tuple[Move, ...],
    ) -> None:
        found_move = False

        # set() prevents duplicate branches for doubles.
        for die in sorted(set(remaining), reverse=True):
            moves = legal_moves_for_die(position, player, die)

            if not moves:
                continue

            found_move = True

            next_remaining = list(remaining)
            next_remaining.remove(die)

            for move in moves:
                next_position = apply_move(position, player, move)

                search(
                    next_position,
                    tuple(next_remaining),
                    sequence + (move,),
                )

        if not found_move:
            sequences.append(sequence)

    search(board, remaining_dice, ())

    maximum_moves = max(len(sequence) for sequence in sequences)

    if maximum_moves == 0:
        return []

    # Backgammon requires using as many dice as possible.
    sequences = [
        sequence
        for sequence in sequences
        if len(sequence) == maximum_moves
    ]

    # If only one of two different dice can be played,
    # the higher die must be used.
    if die_one != die_two and maximum_moves == 1:
        higher_die = max(dice)

        higher_die_sequences = [
            sequence
            for sequence in sequences
            if sequence[0].die == higher_die
        ]

        if higher_die_sequences:
            sequences = higher_die_sequences

    # Remove any exact duplicates while preserving order.
    return list(dict.fromkeys(sequences))