import unittest
from Model.game import Game
from Model.board import OPEN_SPACE, PEG

# AC 4.1: Given the player selects a valid move, when the move is submitted,
# then the game state updates and the board re-renders accordingly.
# STATUS: PASSES

class TestAC4_1(unittest.TestCase):
    def test_valid_move_decrements_peg_count(self):
        game = Game()
        game.new_game()
        initial_pegs = game.peg_count()
        game.handle_click(1, 3)
        game.handle_click(3, 3)
        self.assertEqual(game.peg_count(), initial_pegs - 1)

    def test_valid_move_increments_moves_made(self):
        game = Game()
        game.new_game()
        game.handle_click(1, 3)
        game.handle_click(3, 3)
        self.assertEqual(game.moves_made, 1)

    def test_valid_move_updates_board_cells(self):
        game = Game()
        game.new_game()
        # (1,3) jumps over (2,3) to land on (3,3)
        game.handle_click(1, 3)
        game.handle_click(3, 3)
        self.assertEqual(game.board.grid[1][3], OPEN_SPACE)  # from cell emptied
        self.assertEqual(game.board.grid[2][3], OPEN_SPACE)  # jumped peg removed
        self.assertEqual(game.board.grid[3][3], PEG)          # landing cell filled

if __name__ == "__main__":
    unittest.main()
