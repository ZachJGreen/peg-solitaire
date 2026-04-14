import unittest
from Model.game import ManualGame

# AC 4.2: Given the player attempts an invalid move, when the move is submitted,
# then the game rejects the move and displays feedback without altering game state.
# STATUS: PARTIALLY PASSES — game state is preserved, but no feedback is displayed to the player

class TestAC4_2(unittest.TestCase):
    def test_invalid_move_does_not_change_peg_count(self):
        game = ManualGame()
        game.new_game()
        initial_pegs = game.peg_count()
        # Select (0,2), then click (3,3) — not a valid jump from (0,2)
        game.handle_click(0, 2)
        game.handle_click(3, 3)
        self.assertEqual(game.peg_count(), initial_pegs)

    def test_invalid_move_does_not_increment_moves(self):
        game = ManualGame()
        game.new_game()
        game.handle_click(0, 2)
        game.handle_click(3, 3)
        self.assertEqual(game.moves_made, 0)

    def test_invalid_move_does_not_alter_board_grid(self):
        game = ManualGame()
        game.new_game()
        snapshot = [row[:] for row in game.board.grid]
        game.handle_click(0, 2)
        game.handle_click(3, 3)
        self.assertEqual(game.board.grid, snapshot)

if __name__ == "__main__":
    unittest.main()
