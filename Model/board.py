import math

NOT_PLAYED = -1
PEG = 1
OPEN_SPACE = 0

class Board:
    def __init__(self, type="english", size=7):
        self.type = type
        self.size = size
        self.grid = self.draw_board()

    def draw_board(self):
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
