import random
from Model.board import Board, PEG, OPEN_SPACE


class Game:
    """Base class for both Manual and Automated game modes.
    Holds shared state: board, move counter, and move history."""

    def __init__(self):
        self.board = None
        self.moves_made = 0
        self.history = []

    def new_game(self, board_type="english", size=7):
        self.board = Board(board_type, size)
        self.moves_made = 0
        self.history = []

    def is_game_over(self):
        return self.board is not None and self.board.is_game_over()

    def peg_count(self):
        return self.board.peg_count() if self.board else 0

    def randomize(self):
        """Randomize the current board state and reset counters."""
        if self.board is not None:
            self.board.randomize()
            self.moves_made = 0
            self.history = []

    def _execute_move(self, fr, fc, tr, tc):
        self.board.make_move(fr, fc, tr, tc)
        self.moves_made += 1
        self.history.append((fr, fc, tr, tc))


class ManualGame(Game):
    """Game mode where the human player makes moves by clicking pegs."""

    def __init__(self):
        super().__init__()
        self.selected = None

    def new_game(self, board_type="english", size=7):
        super().new_game(board_type, size)
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

    def make_auto_move(self):
        """Pick and execute one random valid move. Returns True if a move was made."""
        if self.board is None or self.is_game_over():
            return False
        moves = self.board.get_valid_moves()
        if not moves:
            return False
        fr, fc, tr, tc = random.choice(moves)
        self._execute_move(fr, fc, tr, tc)
        return True
