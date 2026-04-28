import inspect

from Model.game import ManualGame
from Model.recorded_game_session import RecordedGameSession
from View.game_controls_view import GameControlsView
from View.main_window import MainWindow
from View.menu_view import MenuView
from View.recorded_games_view import format_recorded_games


class FakeBoardInfo:
    def get_type(self):
        return "english"

    def get_size(self):
        return 7

    def is_recording_enabled(self):
        return True


class FakeMenu:
    board_info = FakeBoardInfo()


def make_window():
    window = MainWindow.__new__(MainWindow)
    window._menu = FakeMenu()
    window._game = ManualGame()
    window._recorded_games = RecordedGameSession()
    window._current_game_recorded = False
    window._autoplay_running = False
    window._refresh = lambda: None
    return window


class TestRecordedGamesUIFlow:
    def test_main_window_initializes_blank_recorded_games_session(self):
        window = make_window()

        assert window._recorded_games.games == []

    def test_start_new_game_records_previous_recorded_game(self):
        window = make_window()
        window._game.new_game(recording_enabled=True)
        window._game.handle_click(1, 3)
        window._game.handle_click(3, 3)

        window._start_new_game()

        assert len(window._recorded_games.games) == 1
        assert window._recorded_games.games[0].moves == [(1, 3, 3, 3)]

    def test_record_current_game_only_records_once(self):
        window = make_window()
        window._game.new_game(recording_enabled=True)
        window._game.handle_click(1, 3)
        window._game.handle_click(3, 3)

        assert window._record_current_game()
        assert not window._record_current_game()

        assert len(window._recorded_games.games) == 1

    def test_game_controls_accept_recorded_games_callback(self):
        signature = inspect.signature(GameControlsView.__init__)
        source = inspect.getsource(GameControlsView)

        assert "on_show_recorded_games" in signature.parameters
        assert "Recorded Games" in source
        assert "command=on_show_recorded_games" in source

    def test_menu_view_passes_recorded_games_callback(self):
        signature = inspect.signature(MenuView.__init__)
        source = inspect.getsource(MenuView)

        assert "on_show_recorded_games" in signature.parameters
        assert "on_show_recorded_games" in source

    def test_format_recorded_games_shows_empty_session_message(self):
        assert format_recorded_games([]) == "No recorded games this session."

    def test_format_recorded_games_lists_recorded_moves(self):
        window = make_window()
        window._game.new_game(board_type="english", size=7, recording_enabled=True)
        window._game.handle_click(1, 3)
        window._game.handle_click(3, 3)
        window._record_current_game()

        text = format_recorded_games(window._recorded_games.games)

        assert "Game 1: English board, size 7" in text
        assert "1. (1, 3) -> (3, 3)" in text
