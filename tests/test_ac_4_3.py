import unittest
from Model.game import Game
from Model.board import NOT_PLAYED, OPEN_SPACE, PEG

# AC 4.3: Given a move results in a win or end condition, when the move is submitted,
# then the game detects it and notifies the player.
# STATUS: PASSES (detection only — UI notification tested manually)

def setup_two_peg_board(game):
    """Helper: clear the board and place two pegs that can make one final move."""
    for r in range(game.board.size):
        for c in range(game.board.size):
            if game.board.grid[r][c] != NOT_PLAYED:
                game.board.grid[r][c] = OPEN_SPACE
    # (3,2) jumps over (3,3) to land on (3,4)
    game.board.grid[3][2] = PEG
    game.board.grid[3][3] = PEG

class TestAC4_3(unittest.TestCase):
    def test_final_move_triggers_game_over(self):
        game = Game()
        game.new_game()
        setup_two_peg_board(game)
        game.handle_click(3, 2)
        game.handle_click(3, 4)
        self.assertTrue(game.is_game_over())

    def test_winning_move_leaves_one_peg(self):
        game = Game()
        game.new_game()
        setup_two_peg_board(game)
        game.handle_click(3, 2)
        game.handle_click(3, 4)
        self.assertEqual(game.peg_count(), 1)

if __name__ == "__main__":
    unittest.main()
