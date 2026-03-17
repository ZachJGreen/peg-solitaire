import unittest
from Model.game import Game
from Model.board import NOT_PLAYED, OPEN_SPACE, PEG

# AC 5.3: Given the game has ended, when the final state is displayed,
# then the board is locked and no further moves can be made.
# STATUS: FAILS — handle_click() still accepts input after game over

def setup_two_peg_board(game):
    for r in range(game.board.size):
        for c in range(game.board.size):
            if game.board.grid[r][c] != NOT_PLAYED:
                game.board.grid[r][c] = OPEN_SPACE
    game.board.grid[3][2] = PEG
    game.board.grid[3][3] = PEG

class TestAC5_3(unittest.TestCase):
    def test_board_locked_after_game_over(self):
        game = Game()
        game.new_game()
        setup_two_peg_board(game)
        game.handle_click(3, 2)
        game.handle_click(3, 4)
        self.assertTrue(game.is_game_over())

        final_grid = [row[:] for row in game.board.grid]
        final_moves = game.moves_made

        # Attempt further input — should be fully ignored
        game.handle_click(3, 4)
        self.assertEqual(game.board.grid, final_grid, "Board grid should not change after game over")
        self.assertEqual(game.moves_made, final_moves, "Move count should not change after game over")
        self.assertIsNone(game.selected, "No selection should be allowed after game over")

if __name__ == "__main__":
    unittest.main()
