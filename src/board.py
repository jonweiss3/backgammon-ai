from dataclasses import dataclass, field

WHITE = 1
BLACK = -1


@dataclass
class Board:
    points: list[int] = field(default_factory=lambda: [0] * 24)
    bar: dict[int, int] = field(
        default_factory=lambda: {WHITE: 0, BLACK: 0}
    )
    off: dict[int, int] = field(
        default_factory=lambda: {WHITE: 0, BLACK: 0}
    )

    @classmethod
    def starting_position(cls):
        points = [0] * 24

        # White
        points[23] = 2
        points[12] = 5
        points[7] = 3
        points[5] = 5

        # Black
        points[0] = -2
        points[11] = -5
        points[16] = -3
        points[18] = -5

        return cls(points=points)

    def total_checkers(self, player: int) -> int:
        on_board = sum(
            abs(count)
            for count in self.points
            if count * player > 0
        )

        return on_board + self.bar[player] + self.off[player]