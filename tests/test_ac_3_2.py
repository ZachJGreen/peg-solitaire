import unittest
from Model.board import Board

# AC 3.2: Given the size or type has not been selected (or is invalid),
# when the player attempts to start the game,
# then the system prevents it and displays a prompt.
# STATUS: PASSES — Board raises ValueError for invalid size/type;
#         view layer (main_window) catches this and shows an error dialog.

class TestAC3_2(unittest.TestCase):
    def test_invalid_size_raises_error(self):
        with self.assertRaises(ValueError):
            Board(size=2)

    def test_non_integer_size_raises_error(self):
        with self.assertRaises((ValueError, TypeError)):
            Board(size="abc")

    def test_invalid_type_raises_error(self):
        with self.assertRaises(ValueError):
            Board(type="triangle", size=7)

    def test_valid_size_and_type_does_not_raise(self):
        board = Board(type="english", size=7)
        self.assertIsNotNone(board)

if __name__ == "__main__":
    unittest.main()
