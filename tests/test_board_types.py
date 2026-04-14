import unittest
from Model.board import Board, NOT_PLAYED, PEG, OPEN_SPACE

# Tests for board type layouts: English, Hexagon, Diamond

class TestEnglishBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(type="english", size=7)

    def test_center_is_open(self):
        self.assertEqual(self.board.grid[3][3], OPEN_SPACE)

    def test_corner_cells_not_played(self):
        self.assertEqual(self.board.grid[0][0], NOT_PLAYED)
        self.assertEqual(self.board.grid[0][6], NOT_PLAYED)
        self.assertEqual(self.board.grid[6][0], NOT_PLAYED)
        self.assertEqual(self.board.grid[6][6], NOT_PLAYED)

    def test_peg_count_at_start(self):
        self.assertEqual(self.board.peg_count(), 32)


class TestHexagonBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(type="hexagon", size=7)

    def test_center_is_open(self):
        self.assertEqual(self.board.grid[3][3], OPEN_SPACE)

    def test_outer_corners_not_played(self):
        # Top-left and bottom-right corners should be NOT_PLAYED
        self.assertEqual(self.board.grid[0][0], NOT_PLAYED)
        self.assertEqual(self.board.grid[6][6], NOT_PLAYED)

    def test_top_row_has_fewer_cells_than_middle(self):
        top_pegs = sum(1 for c in self.board.grid[0] if c != NOT_PLAYED)
        mid_pegs = sum(1 for c in self.board.grid[3] if c != NOT_PLAYED)
        self.assertLess(top_pegs, mid_pegs)

    def test_hexagon_is_symmetric(self):
        for r in range(self.board.size):
            mirror = self.board.size - 1 - r
            self.assertEqual(self.board.grid[r], self.board.grid[mirror])


class TestDiamondBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(type="diamond", size=7)

    def test_center_is_open(self):
        self.assertEqual(self.board.grid[3][3], OPEN_SPACE)

    def test_corners_not_played(self):
        self.assertEqual(self.board.grid[0][0], NOT_PLAYED)
        self.assertEqual(self.board.grid[0][6], NOT_PLAYED)

    def test_top_row_has_one_valid_cell(self):
        valid = [c for c in self.board.grid[0] if c != NOT_PLAYED]
        self.assertEqual(len(valid), 1)

    def test_middle_row_is_full(self):
        valid = [c for c in self.board.grid[3] if c != NOT_PLAYED]
        self.assertEqual(len(valid), 7)

    def test_diamond_is_symmetric(self):
        for r in range(self.board.size):
            mirror = self.board.size - 1 - r
            self.assertEqual(self.board.grid[r], self.board.grid[mirror])


if __name__ == "__main__":
    unittest.main()
