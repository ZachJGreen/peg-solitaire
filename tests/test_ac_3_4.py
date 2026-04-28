from Model.game import ManualGame

# AC 3.4: Given the player is mid-game, when the player chooses to start a new game,
# then the system prompts for confirmation before discarding the current state.
# STATUS: PASSES — moves_made > 0 signals mid-game state; the view layer
#         (main_window._on_new_game) reads this and shows a confirmation dialog.

class TestAC3_4:
    def test_mid_game_state_is_detectable(self):
        """The model exposes moves_made so the view can trigger a confirmation prompt."""
        game = ManualGame()
        game.new_game()
        game.handle_click(1, 3)
        game.handle_click(3, 3)
        assert game.moves_made > 0, "moves_made > 0 signals mid-game; view uses this to prompt confirmation"

    def test_new_game_fully_resets_after_confirmation(self):
        """Once the view confirms, calling new_game() should fully clear state."""
        game = ManualGame()
        game.new_game()
        game.handle_click(1, 3)
        game.handle_click(3, 3)
        game.new_game()
        assert game.moves_made == 0
        assert game.selected is None
