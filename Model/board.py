import math
import random

NOT_PLAYED = -1
PEG = 1
OPEN_SPACE = 0

VALID_TYPES = ("english", "hexagon", "diamond")

class Board:
    def __init__(self, type="english", size=7):
        if not isinstance(size, int) or size < 3:
            raise ValueError(f"Invalid board size: {size}. Must be an integer >= 3.")
        if type not in VALID_TYPES:
            raise ValueError(f"Invalid board type: {type}. Must be one of {VALID_TYPES}.")
        self.type = type
        self.size = size
        self.grid = self.draw_board()

    def draw_board(self):
        if self.type == "hexagon":
            return self._draw_hexagon()
        elif self.type == "diamond":
            return self._draw_diamond()
        else:
            return self._draw_english()

    def _draw_english(self):
        size = self.size
        null_spaces = (math.ceil(size / 2)) / 2
        board = []
        for row in range(size):
            row_list = []
            for col in range(size):
                if ((col < null_spaces or col >= (size - null_spaces)) and
                        (row < null_spaces or row >= (size - null_spaces))):
                    row_list.append(NOT_PLAYED)
                elif (row, col) == (size // 2, size // 2):
                    row_list.append(OPEN_SPACE)
                else:
                    row_list.append(PEG)
            board.append(row_list)
        return board

    def _draw_hexagon(self):
        # Hexagon shape: corner cuts taper diagonally — each row closer to
        # the top/bottom gets 1 more null column per side than the row below/above.
        size = self.size
        half = size // 2
        board = []
        for row in range(size):
            null_cols = max(0, half - 1 - min(row, size - 1 - row))
            row_list = []
            for col in range(size):
                if col < null_cols or col >= (size - null_cols):
                    row_list.append(NOT_PLAYED)
                elif (row, col) == (size // 2, size // 2):
                    row_list.append(OPEN_SPACE)
                else:
                    row_list.append(PEG)
            board.append(row_list)
        return board

    def _draw_diamond(self):
        # Diamond shape: null columns per side equal the distance from the middle row.
        size = self.size
        half = size // 2
        board = []
        for row in range(size):
            null_cols = abs(row - half)
            row_list = []
            for col in range(size):
                if col < null_cols or col >= (size - null_cols):
                    row_list.append(NOT_PLAYED)
                elif (row, col) == (size // 2, size // 2):
                    row_list.append(OPEN_SPACE)
                else:
                    row_list.append(PEG)
            board.append(row_list)
        return board

    def get_valid_moves(self):
        moves = []
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == PEG:
                    for dr, dc in directions:
                        mr, mc = r + dr // 2, c + dc // 2
                        tr, tc = r + dr, c + dc
                        if (0 <= tr < self.size and 0 <= tc < self.size
                                and self.grid[mr][mc] == PEG
                                and self.grid[tr][tc] == OPEN_SPACE):
                            moves.append((r, c, tr, tc))
        return moves

    def make_move(self, fr, fc, tr, tc):
        mr, mc = (fr + tr) // 2, (fc + tc) // 2
        self.grid[fr][fc] = OPEN_SPACE
        self.grid[mr][mc] = OPEN_SPACE
        self.grid[tr][tc] = PEG

    def peg_count(self):
        return sum(cell == PEG for row in self.grid for cell in row)

    def is_game_over(self):
        return len(self.get_valid_moves()) == 0

    def randomize(self, num_moves=20):
        """Apply random valid moves to produce a randomized board state."""
        for _ in range(num_moves):
            moves = self.get_valid_moves()
            if not moves:
                break
            fr, fc, tr, tc = random.choice(moves)
            self.make_move(fr, fc, tr, tc)
