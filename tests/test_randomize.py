import unittest
from Model.game import ManualGame, AutomatedGame

# User Story 8: Randomize the state of the board during a manual game

class TestRandomize(unittest.TestCase):
    def test_randomize_changes_board_state(self):
        game = ManualGame()
        game.new_game()
        initial_grid = [row[:] for row in game.board.grid]
        game.randomize()
        self.assertNotEqual(game.board.grid, initial_grid,
                            "Board should change after randomization")

    def test_randomize_reduces_peg_count(self):
        game = ManualGame()
        game.new_game()
        initial_pegs = game.peg_count()
        game.randomize()
        # Randomize applies moves, so peg count should be lower
        self.assertLess(game.peg_count(), initial_pegs)

    def test_randomize_resets_move_counter(self):
        game = ManualGame()
        game.new_game()
        game.handle_click(1, 3)
        game.handle_click(3, 3)
        game.randomize()
        self.assertEqual(game.moves_made, 0)

    def test_randomize_resets_history(self):
        game = ManualGame()
        game.new_game()
        game.handle_click(1, 3)
        game.handle_click(3, 3)
        game.randomize()
        self.assertEqual(game.history, [])

    def test_randomize_available_on_automated_game(self):
        game = AutomatedGame()
        game.new_game()
        initial_grid = [row[:] for row in game.board.grid]
        game.randomize()
        self.assertNotEqual(game.board.grid, initial_grid)

if __name__ == "__main__":
    unittest.main()
