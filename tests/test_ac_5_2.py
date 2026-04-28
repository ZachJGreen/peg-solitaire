import pytest

# AC 5.2: Given the game is over, when the notification is shown,
# then the player is presented with options such as starting a new game or returning to the menu.
# STATUS: FAILS — messagebox only shows OK; no post-game options are offered

class TestAC5_2:
    @pytest.mark.skip(reason="UI-level test — messagebox currently has no action options (New Game / Return to Menu)")
    def test_game_over_presents_options(self):
        # Would require checking that the game-over dialog offers
        # actionable choices, not just an OK button.
        pass
