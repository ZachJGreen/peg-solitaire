from dataclasses import dataclass


@dataclass(frozen=True)
class RecordedGame:
    board_type: str
    size: int
    moves: list
    events: list
    starting_grid: list
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
        events = _copy_events(getattr(game, "recorded_events", []))
        if not events or game.board is None:
            return False

        self.games.append(RecordedGame(
            board_type=game.board.type,
            size=game.board.size,
            moves=moves,
            events=events,
            starting_grid=_copy_grid(game.starting_grid),
            remaining_pegs=game.peg_count(),
            won=game.peg_count() == 1,
        ))
        return True


def _copy_grid(grid):
    return [row[:] for row in grid]


def _copy_events(events):
    copied = []
    for event in events:
        if event["type"] == "move":
            copied.append({
                "type": "move",
                "from": tuple(event["from"]),
                "to": tuple(event["to"]),
            })
        elif event["type"] == "randomize":
            copied.append({
                "type": "randomize",
                "grid": _copy_grid(event["grid"]),
            })
    return copied
