from Model.game import ManualGame
from View.main_window import MainWindow


class FakeBoardInfo:
    def __init__(self, recording_enabled=True):
        self.recording_enabled = recording_enabled

    def get_type(self):
        return "english"

    def get_size(self):
        return 7

    def is_recording_enabled(self):
        return self.recording_enabled


class FakeMenu:
    def __init__(self, recording_enabled=True):
        self.board_info = FakeBoardInfo(recording_enabled)


def make_window(recording_enabled=True):
    window = MainWindow.__new__(MainWindow)
    window._menu = FakeMenu(recording_enabled)
    window._game = ManualGame()
    window._autoplay_running = False
    window._refresh = lambda: None
    return window


class TestMainWindowRecordingFlow:
    def test_start_new_game_uses_recording_checkbox_value(self):
        window = make_window(recording_enabled=False)

        window._start_new_game()

        assert not window._game.recording_enabled

    def test_changing_checkbox_mid_game_does_not_change_active_recording(self):
        window = make_window(recording_enabled=True)
        window._start_new_game()

        window._menu.board_info.recording_enabled = False

        assert window._game.recording_enabled

    def test_next_new_game_uses_changed_checkbox_value(self):
        window = make_window(recording_enabled=True)
        window._start_new_game()
        window._menu.board_info.recording_enabled = False

        window._start_new_game()

        assert not window._game.recording_enabled

    def test_autoplay_preserves_recording_state_and_recorded_moves(self):
        window = make_window(recording_enabled=True)
        window._start_new_game()
        window._game.handle_click(1, 3)
        window._game.handle_click(3, 3)
        window._run_autoplay = lambda: None

        window._on_autoplay()

        assert window._game.recording_enabled
        assert window._game.recorded_moves == [(1, 3, 3, 3)]
