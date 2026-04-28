from Model.board import NOT_PLAYED, OPEN_SPACE, PEG
from Model.game import AutomatedGame, ManualGame
from Model.recorded_game_session import RecordedGameSession
from View.game_over_dialog import GAME_OVER_RANDOMIZE_LIMIT
from View.main_window import MainWindow


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
    window._game.new_game(recording_enabled=True)
    window._recorded_games = RecordedGameSession()
    window._current_game_recorded = False
    window._game_over_randomizes_remaining = GAME_OVER_RANDOMIZE_LIMIT
    window.refresh_count = 0
    window._refresh = lambda: setattr(window, "refresh_count", window.refresh_count + 1)
    return window


def force_single_peg_game_over(game):
    for r in range(game.board.size):
        for c in range(game.board.size):
            if game.board.grid[r][c] != NOT_PLAYED:
                game.board.grid[r][c] = OPEN_SPACE
    game.board.grid[3][3] = PEG


class TestGameOverRecoveryRandomize:
    def test_recovery_randomize_spends_one_attempt(self):
        window = make_window()
        force_single_peg_game_over(window._game)

        recovered, remaining = window._try_game_over_randomize()

        assert not recovered
        assert remaining == GAME_OVER_RANDOMIZE_LIMIT - 1
        assert window.refresh_count == 1

    def test_recovery_randomize_stops_after_three_attempts(self):
        window = make_window()
        force_single_peg_game_over(window._game)

        for _ in range(GAME_OVER_RANDOMIZE_LIMIT):
            window._try_game_over_randomize()

        assert window._game_over_randomizes_remaining == 0
        assert window._try_game_over_randomize() == (False, 0)
        assert window.refresh_count == GAME_OVER_RANDOMIZE_LIMIT

    def test_recovery_randomize_reports_recovered_when_moves_exist(self):
        window = make_window()

        assert window._try_game_over_randomize()[0]

    def test_recovery_randomize_reports_not_recovered_when_no_move_can_exist(self):
        window = make_window()
        force_single_peg_game_over(window._game)

        assert not window._try_game_over_randomize()[0]
        assert window._game.is_game_over()

    def test_recovered_autoplay_game_schedules_autoplay_to_continue(self):
        window = make_window()
        automated = AutomatedGame()
        automated.new_game()
        window._game = automated
        window.after_calls = []
        window.after = lambda delay, callback: window.after_calls.append((delay, callback))
        window._run_autoplay = lambda: None

        recovered, _remaining = window._try_game_over_randomize()

        assert recovered
        assert window._autoplay_running
        assert len(window.after_calls) == 1

    def test_recovery_randomize_is_recorded_when_game_is_closed(self):
        window = make_window()
        window._game.handle_click(1, 3)
        window._game.handle_click(3, 3)

        window._try_game_over_randomize()
        assert window._record_current_game()

        recorded = window._recorded_games.games[0]
        assert [event["type"] for event in recorded.events] == ["move", "randomize"]
        assert recorded.moves == [(1, 3, 3, 3)]

    def test_sidebar_new_game_records_recovery_randomize_before_replacing_game(self):
        window = make_window()
        window._game.handle_click(1, 3)
        window._game.handle_click(3, 3)
        window._try_game_over_randomize()

        window._start_new_game()

        recorded = window._recorded_games.games[0]
        assert [event["type"] for event in recorded.events] == ["move", "randomize"]
