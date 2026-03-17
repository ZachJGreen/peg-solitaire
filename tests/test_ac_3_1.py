import unittest
from Model.game import Game

# AC 3.1: Given the player selects a valid size/type, when confirmed,
# then a new game starts with the selected board size and type.
# STATUS: PASSES

class TestAC3_1(unittest.TestCase):
    def test_new_game_initializes_board(self):
        game = Game()
        game.new_game()
        self.assertIsNotNone(game.board)
        self.assertEqual(game.board.size, 7)
        self.assertEqual(game.board.type, "english")

if __name__ == "__main__":
    unittest.main()
