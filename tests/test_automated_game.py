import unittest
from Model.game import AutomatedGame
from Model.board import NOT_PLAYED, OPEN_SPACE, PEG

# Tests for AutomatedGame — computer-controlled move selection

class TestAutomatedGame(unittest.TestCase):
    def test_make_auto_move_reduces_peg_count(self):
        game = AutomatedGame()
        game.new_game()
        pegs_before = game.peg_count()
        game.make_auto_move()
        self.assertEqual(game.peg_count(), pegs_before - 1)

    def test_make_auto_move_increments_moves_made(self):
        game = AutomatedGame()
        game.new_game()
        game.make_auto_move()
        self.assertEqual(game.moves_made, 1)

    def test_make_auto_move_records_history(self):
        game = AutomatedGame()
        game.new_game()
        game.make_auto_move()
        self.assertEqual(len(game.history), 1)

    def test_make_auto_move_returns_true_when_move_made(self):
        game = AutomatedGame()
        game.new_game()
        result = game.make_auto_move()
        self.assertTrue(result)

    def test_make_auto_move_returns_false_when_game_over(self):
        game = AutomatedGame()
        game.new_game()
        # Force game over: clear board, leave no valid moves
        for r in range(game.board.size):
            for c in range(game.board.size):
                if game.board.grid[r][c] != NOT_PLAYED:
                    game.board.grid[r][c] = OPEN_SPACE
        game.board.grid[3][3] = PEG  # single peg, no moves possible
        result = game.make_auto_move()
        self.assertFalse(result)

    def test_automated_game_detects_game_over(self):
        game = AutomatedGame()
        game.new_game()
        for r in range(game.board.size):
            for c in range(game.board.size):
                if game.board.grid[r][c] != NOT_PLAYED:
                    game.board.grid[r][c] = OPEN_SPACE
        game.board.grid[3][3] = PEG
        self.assertTrue(game.is_game_over())

    def test_automated_game_accepts_hexagon_board(self):
        game = AutomatedGame()
        game.new_game(board_type="hexagon", size=7)
        self.assertEqual(game.board.type, "hexagon")
        result = game.make_auto_move()
        self.assertTrue(result)

    def test_automated_game_accepts_diamond_board(self):
        game = AutomatedGame()
        game.new_game(board_type="diamond", size=7)
        self.assertEqual(game.board.type, "diamond")
        result = game.make_auto_move()
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
