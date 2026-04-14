import unittest
from Model.game import ManualGame
from Model.board import NOT_PLAYED, OPEN_SPACE, PEG

# AC 5.1: Given the end condition is met, when the game ends,
# then the player is clearly notified of the outcome.
# STATUS: PASSES (detection only — UI messagebox notification tested manually)

def setup_two_peg_board(game):
    for r in range(game.board.size):
        for c in range(game.board.size):
            if game.board.grid[r][c] != NOT_PLAYED:
                game.board.grid[r][c] = OPEN_SPACE
    game.board.grid[3][2] = PEG
    game.board.grid[3][3] = PEG

class TestAC5_1(unittest.TestCase):
    def test_game_detects_end_condition(self):
        game = ManualGame()
        game.new_game()
        setup_two_peg_board(game)
        game.handle_click(3, 2)
        game.handle_click(3, 4)
        self.assertTrue(game.is_game_over())

    def test_game_not_over_at_start(self):
        game = ManualGame()
        game.new_game()
        self.assertFalse(game.is_game_over())

if __name__ == "__main__":
    unittest.main()
