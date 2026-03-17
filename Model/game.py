from Model.board import Board, PEG, OPEN_SPACE

class Game:
    def __init__(self):
        self.board = None
        self.moves_made = 0
        self.selected = None

    def new_game(self):
        self.board = Board()
        self.moves_made = 0
        self.selected = None

    def handle_click(self, row, col):
        if self.board is None:
            return
        cell = self.board.grid[row][col]

        if self.selected is None:
            if cell == PEG:
                self.selected = (row, col)
            return

        sr, sc = self.selected
        if (sr, sc, row, col) in self.board.get_valid_moves():
            self.board.make_move(sr, sc, row, col)
            self.moves_made += 1
            self.selected = None
        elif cell == PEG:
            self.selected = (row, col)
        else:
            self.selected = None

    def is_game_over(self):
        return self.board is not None and self.board.is_game_over()

    def peg_count(self):
        return self.board.peg_count() if self.board else 0
