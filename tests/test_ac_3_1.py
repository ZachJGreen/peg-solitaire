import unittest
from Model.game import ManualGame

# AC 3.1: Given the player selects a valid size/type, when confirmed,
# then a new game starts with the selected board size and type.
# STATUS: PASSES

class TestAC3_1(unittest.TestCase):
    def test_new_game_initializes_board(self):
        game = ManualGame()
        game.new_game()
        self.assertIsNotNone(game.board)
        self.assertEqual(game.board.size, 7)
        self.assertEqual(game.board.type, "english")

    def test_new_game_accepts_custom_size_and_type(self):
        game = ManualGame()
        game.new_game(board_type="hexagon", size=9)
        self.assertEqual(game.board.size, 9)
        self.assertEqual(game.board.type, "hexagon")

    def test_new_game_accepts_diamond_type(self):
        game = ManualGame()
        game.new_game(board_type="diamond", size=7)
        self.assertEqual(game.board.type, "diamond")

if __name__ == "__main__":
    unittest.main()
