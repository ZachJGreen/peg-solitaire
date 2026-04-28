from Model.game import ManualGame
from Model.board import NOT_PLAYED, OPEN_SPACE, PEG

# AC 4.4: Given the game is over, when the player attempts a move,
# then the system rejects the input.
# STATUS: PASSES — handle_click() checks is_game_over() before processing input

def setup_two_peg_board(game):
    for r in range(game.board.size):
        for c in range(game.board.size):
            if game.board.grid[r][c] != NOT_PLAYED:
                game.board.grid[r][c] = OPEN_SPACE
    game.board.grid[3][2] = PEG
    game.board.grid[3][3] = PEG

class TestAC4_4:
    def test_click_after_game_over_does_not_change_selection(self):
        game = ManualGame()
        game.new_game()
        setup_two_peg_board(game)
        game.handle_click(3, 2)
        game.handle_click(3, 4)
        assert game.is_game_over()

        # Input after game over should be fully rejected
        game.handle_click(3, 4)  # click the remaining peg
        assert game.selected is None, "No selection should occur after game is over"

    def test_click_after_game_over_does_not_change_move_count(self):
        game = ManualGame()
        game.new_game()
        setup_two_peg_board(game)
        game.handle_click(3, 2)
        game.handle_click(3, 4)
        moves_at_end = game.moves_made
        game.handle_click(3, 4)
        assert game.moves_made == moves_at_end
