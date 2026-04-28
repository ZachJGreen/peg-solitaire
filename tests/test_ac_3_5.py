from Model.game import ManualGame

# AC 3.5: Given the player confirms a new game, when the game initializes,
# then all previous game states are fully cleared.
# STATUS: PASSES

class TestAC3_5:
    def test_previous_board_is_replaced(self):
        game = ManualGame()
        game.new_game()
        old_board = game.board
        game.new_game()
        assert game.board is not old_board

    def test_selection_is_cleared(self):
        game = ManualGame()
        game.new_game()
        game.handle_click(1, 3)  # select a peg
        game.new_game()
        assert game.selected is None

    def test_moves_are_cleared(self):
        game = ManualGame()
        game.new_game()
        game.handle_click(1, 3)
        game.handle_click(3, 3)
        game.new_game()
        assert game.moves_made == 0

    def test_history_is_cleared(self):
        game = ManualGame()
        game.new_game()
        game.handle_click(1, 3)
        game.handle_click(3, 3)
        game.new_game()
        assert game.history == []
