import random
from Model.board import Board, PEG, OPEN_SPACE


def copy_grid(grid):
    return [row[:] for row in grid]


class Game:
    """Base class for both Manual and Automated game modes.
    Holds shared state: board, move counter, and move history."""

    def __init__(self):
        self.board = None
        self.moves_made = 0
        self.history = []
        self.redo_history = []
        self.recording_enabled = True
        self.recorded_moves = []
        self.recorded_events = []
        self.starting_grid = None

    def new_game(self, board_type="english", size=7, recording_enabled=True):
        self.board = Board(board_type, size)
        self.moves_made = 0
        self.history = []
        self.redo_history = []
        self.recording_enabled = recording_enabled
        self.recorded_moves = []
        self.recorded_events = []
        self.starting_grid = copy_grid(self.board.grid)

    def is_game_over(self):
        return self.board is not None and self.board.is_game_over()

    def peg_count(self):
        return self.board.peg_count() if self.board else 0

    def randomize(self):
        """Randomize the current board state and reset counters."""
        if self.board is not None:
            changed = self.board.randomize()
            self.moves_made = 0
            self.history = []
            self.redo_history = []
            if changed and self.recording_enabled:
                self.recorded_events.append({
                    "type": "randomize",
                    "grid": copy_grid(self.board.grid),
                })
            return changed
        return False

    def _execute_move(self, fr, fc, tr, tc):
        self._apply_move(fr, fc, tr, tc)
        self.redo_history = []

    def _apply_move(self, fr, fc, tr, tc):
        self.board.make_move(fr, fc, tr, tc)
        self.moves_made += 1
        self.history.append((fr, fc, tr, tc))
        if self.recording_enabled:
            self.recorded_moves.append((fr, fc, tr, tc))
            self.recorded_events.append({
                "type": "move",
                "from": (fr, fc),
                "to": (tr, tc),
            })

    def undo_move(self):
        if self.board is None or not self.history:
            return False

        fr, fc, tr, tc = self.history.pop()
        mr, mc = (fr + tr) // 2, (fc + tc) // 2
        self.board.grid[fr][fc] = PEG
        self.board.grid[mr][mc] = PEG
        self.board.grid[tr][tc] = OPEN_SPACE
        self.moves_made -= 1
        self.redo_history.append((fr, fc, tr, tc))
        if self.recording_enabled and self.recorded_moves:
            self.recorded_moves.pop()
        if self.recording_enabled and self.recorded_events:
            self.recorded_events.pop()
        return True

    def redo_move(self):
        if self.board is None or not self.redo_history:
            return False

        fr, fc, tr, tc = self.redo_history.pop()
        self._apply_move(fr, fc, tr, tc)
        return True


class ManualGame(Game):
    """Game mode where the human player makes moves by clicking pegs."""

    def __init__(self):
        super().__init__()
        self.selected = None

    def new_game(self, board_type="english", size=7, recording_enabled=True):
        super().new_game(board_type, size, recording_enabled)
        self.selected = None

    def handle_click(self, row, col):
        if self.board is None or self.is_game_over():
            return

        cell = self.board.grid[row][col]

        if self.selected is None:
            if cell == PEG:
                self.selected = (row, col)
            return

        sr, sc = self.selected
        if (sr, sc, row, col) in self.board.get_valid_moves():
            self._execute_move(sr, sc, row, col)
            self.selected = None
        elif cell == PEG:
            self.selected = (row, col)
        else:
            self.selected = None


class AutomatedGame(Game):
    """Game mode where the computer selects and executes moves automatically."""

    def __init__(self):
        super().__init__()
        self.replay_events = None
        self.replay_index = 0

    def load_replay(self, recorded_game):
        self.board = Board(recorded_game.board_type, recorded_game.size)
        self.board.grid = copy_grid(recorded_game.starting_grid)
        self.moves_made = 0
        self.history = []
        self.redo_history = []
        self.recording_enabled = False
        self.recorded_moves = []
        self.recorded_events = []
        self.starting_grid = copy_grid(recorded_game.starting_grid)
        self.replay_events = list(recorded_game.events)
        self.replay_index = 0

    def is_replay_active(self):
        return self.replay_events is not None

    def make_auto_move(self):
        """Pick and execute one random valid move. Returns True if a move was made."""
        if self.board is None:
            return False
        if self.replay_events is not None:
            return self._make_replay_move()
        if self.is_game_over():
            return False
        moves = self.board.get_valid_moves()
        if not moves:
            return False
        fr, fc, tr, tc = random.choice(moves)
        self._execute_move(fr, fc, tr, tc)
        return True

    def _make_replay_move(self):
        if self.replay_index >= len(self.replay_events):
            return False

        event = self.replay_events[self.replay_index]
        self.replay_index += 1
        if event["type"] == "move":
            fr, fc = event["from"]
            tr, tc = event["to"]
            self.board.make_move(fr, fc, tr, tc)
            self.moves_made += 1
            self.history.append((fr, fc, tr, tc))
            return True
        if event["type"] == "randomize":
            self.board.grid = copy_grid(event["grid"])
            self.moves_made = 0
            self.history = []
            self.redo_history = []
            return True
        return False
