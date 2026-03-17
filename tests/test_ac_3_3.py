import unittest
from Model.game import Game

# AC 3.3: Given a new game starts, when the board is displayed,
# then moves made resets to 0 and pegs remaining equals the starting peg count.
# STATUS: PASSES

class TestAC3_3(unittest.TestCase):
    def test_moves_reset_to_zero(self):
        game = Game()
        game.new_game()
        game.handle_click(1, 3)
        game.handle_click(3, 3)
        game.new_game()
        self.assertEqual(game.moves_made, 0)

    def test_peg_count_is_correct_at_start(self):
        game = Game()
        game.new_game()
        self.assertEqual(game.peg_count(), 32)

if __name__ == "__main__":
    unittest.main()
