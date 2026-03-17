import unittest
from Model.game import Game

# AC 4.5: Given a valid move is made, when the board updates,
# then the move is recorded in the game's move history.
# STATUS: FAILS — Game has no move history

class TestAC4_5(unittest.TestCase):
    def test_game_has_history_attribute(self):
        game = Game()
        game.new_game()
        self.assertTrue(hasattr(game, 'history'), "Game should have a move history attribute")

    def test_valid_move_recorded_in_history(self):
        game = Game()
        game.new_game()
        game.handle_click(1, 3)
        game.handle_click(3, 3)
        self.assertEqual(len(game.history), 1)

    def test_history_contains_correct_move(self):
        game = Game()
        game.new_game()
        game.handle_click(1, 3)
        game.handle_click(3, 3)
        self.assertEqual(game.history[0], (1, 3, 3, 3))

if __name__ == "__main__":
    unittest.main()
