import unittest
from Model.game import Game

# AC 3.4: Given the player is mid-game, when the player chooses to start a new game,
# then the system prompts for confirmation before discarding the current state.
# STATUS: FAILS — new_game() resets immediately with no confirmation mechanism

class TestAC3_4(unittest.TestCase):
    def test_new_game_mid_game_requires_confirmation(self):
        game = Game()
        game.new_game()
        game.handle_click(1, 3)
        game.handle_click(3, 3)
        self.assertGreater(game.moves_made, 0)

        # Game should expose a way to request a new game and await confirmation
        # rather than resetting immediately
        self.assertTrue(
            hasattr(game, 'request_new_game'),
            "Game should have a request_new_game() method that triggers confirmation"
        )

if __name__ == "__main__":
    unittest.main()
