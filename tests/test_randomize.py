from Model.board import NOT_PLAYED, OPEN_SPACE, PEG
from Model.game import ManualGame, AutomatedGame

# User Story 8: Randomize the state of the board during a manual game

class TestRandomize:
    def test_randomize_changes_board_state(self):
        game = ManualGame()
        game.new_game()
        initial_grid = [row[:] for row in game.board.grid]
        game.randomize()
        assert game.board.grid != initial_grid, "Board should change after randomization"

    def test_randomize_preserves_peg_count(self):
        game = ManualGame()
        game.new_game()
        initial_pegs = game.peg_count()
        game.randomize()
        assert game.peg_count() == initial_pegs

    def test_randomize_preserves_open_space_count(self):
        game = ManualGame()
        game.new_game()
        game.handle_click(1, 3)
        game.handle_click(3, 3)
        initial_open_spaces = sum(
            cell == OPEN_SPACE
            for row in game.board.grid
            for cell in row
        )

        game.randomize()

        assert sum(
            cell == OPEN_SPACE
            for row in game.board.grid
            for cell in row
        ) == initial_open_spaces

    def test_randomize_preserves_not_played_spaces(self):
        game = ManualGame()
        game.new_game()
        initial_not_played = [
            (r, c)
            for r, row in enumerate(game.board.grid)
            for c, cell in enumerate(row)
            if cell == NOT_PLAYED
        ]

        game.randomize()

        assert [
            (r, c)
            for r, row in enumerate(game.board.grid)
            for c, cell in enumerate(row)
            if cell == NOT_PLAYED
        ] == initial_not_played

    def test_randomize_resets_move_counter(self):
        game = ManualGame()
        game.new_game()
        game.handle_click(1, 3)
        game.handle_click(3, 3)
        game.randomize()
        assert game.moves_made == 0

    def test_randomize_resets_history(self):
        game = ManualGame()
        game.new_game()
        game.handle_click(1, 3)
        game.handle_click(3, 3)
        game.randomize()
        assert game.history == []

    def test_randomize_preserves_recorded_move_log_for_replay_summary(self):
        game = ManualGame()
        game.new_game(recording_enabled=True)
        game.handle_click(1, 3)
        game.handle_click(3, 3)
        game.randomize()
        assert game.recorded_moves == [(1, 3, 3, 3)]

    def test_randomize_available_on_automated_game(self):
        game = AutomatedGame()
        game.new_game()
        initial_grid = [row[:] for row in game.board.grid]
        game.randomize()
        assert game.board.grid != initial_grid
