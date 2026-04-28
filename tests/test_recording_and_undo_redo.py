from Model.board import OPEN_SPACE, PEG
from Model.game import ManualGame


class TestRecordingAndUndoRedo:
    def test_new_game_stores_recording_choice(self):
        game = ManualGame()
        game.new_game(recording_enabled=False)

        assert not game.recording_enabled

    def test_recording_enabled_records_valid_moves(self):
        game = ManualGame()
        game.new_game(recording_enabled=True)

        game.handle_click(1, 3)
        game.handle_click(3, 3)

        assert game.recorded_moves == [(1, 3, 3, 3)]

    def test_recording_disabled_keeps_recorded_moves_empty(self):
        game = ManualGame()
        game.new_game(recording_enabled=False)

        game.handle_click(1, 3)
        game.handle_click(3, 3)

        assert game.history == [(1, 3, 3, 3)]
        assert game.recorded_moves == []

    def test_undo_restores_board_and_decrements_move_count(self):
        game = ManualGame()
        game.new_game(recording_enabled=True)

        game.handle_click(1, 3)
        game.handle_click(3, 3)
        assert game.undo_move()

        assert game.moves_made == 0
        assert game.board.grid[1][3] == PEG
        assert game.board.grid[2][3] == PEG
        assert game.board.grid[3][3] == OPEN_SPACE
        assert game.history == []
        assert game.recorded_moves == []

    def test_redo_reapplies_undone_move(self):
        game = ManualGame()
        game.new_game(recording_enabled=True)

        game.handle_click(1, 3)
        game.handle_click(3, 3)
        game.undo_move()
        assert game.redo_move()

        assert game.moves_made == 1
        assert game.board.grid[1][3] == OPEN_SPACE
        assert game.board.grid[2][3] == OPEN_SPACE
        assert game.board.grid[3][3] == PEG
        assert game.history == [(1, 3, 3, 3)]
        assert game.recorded_moves == [(1, 3, 3, 3)]

    def test_new_move_after_undo_clears_redo_stack(self):
        game = ManualGame()
        game.new_game()

        game.handle_click(1, 3)
        game.handle_click(3, 3)
        game.undo_move()
        game.handle_click(3, 1)
        game.handle_click(3, 3)

        assert not game.redo_move()
        assert game.history == [(3, 1, 3, 3)]
