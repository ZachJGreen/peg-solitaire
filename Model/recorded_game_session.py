from dataclasses import dataclass


@dataclass(frozen=True)
class RecordedGame:
    board_type: str
    size: int
    moves: list
    remaining_pegs: int
    won: bool

    @property
    def move_count(self):
        return len(self.moves)


class RecordedGameSession:
    """Stores recorded games for the current application session only."""

    def __init__(self):
        self.games = []

    def add_game(self, game):
        if not getattr(game, "recording_enabled", False):
            return False
        moves = list(getattr(game, "recorded_moves", []))
        if not moves or game.board is None:
            return False

        self.games.append(RecordedGame(
            board_type=game.board.type,
            size=game.board.size,
            moves=moves,
            remaining_pegs=game.peg_count(),
            won=game.peg_count() == 1,
        ))
        return True
