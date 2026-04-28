from Model.game import AutomatedGame, ManualGame
from Model.recorded_game_session import RecordedGame, RecordedGameSession
from View.main_window import MainWindow


def recorded_game_from_manual_game(game):
    session = RecordedGameSession()
    assert session.add_game(game)
    return session.games[0]


def make_window():
    window = MainWindow.__new__(MainWindow)
    window.refresh_count = 0
    window.after_calls = []
    window._refresh = lambda: setattr(window, "refresh_count", window.refresh_count + 1)
    window.after = lambda delay, callback: window.after_calls.append((delay, callback))
    window._autoplay_running = False
    window._replay_completed = False
    return window


class TestRecordedGameReplay:
    def test_scripted_autoplay_replays_recorded_moves_from_starting_grid(self):
        manual = ManualGame()
        manual.new_game(recording_enabled=True)
        manual.handle_click(1, 3)
        manual.handle_click(3, 3)
        recorded = recorded_game_from_manual_game(manual)

        replay = AutomatedGame()
        replay.load_replay(recorded)

        assert replay.board.grid == recorded.starting_grid
        assert replay.make_auto_move()
        assert replay.board.grid == manual.board.grid
        assert not replay.make_auto_move()

    def test_scripted_autoplay_replays_randomize_grid(self):
        manual = ManualGame()
        manual.new_game(recording_enabled=True)
        manual.randomize()
        recorded = recorded_game_from_manual_game(manual)

        replay = AutomatedGame()
        replay.load_replay(recorded)

        assert replay.make_auto_move()
        assert replay.board.grid == manual.board.grid

    def test_main_window_replay_starts_scripted_autoplay(self):
        manual = ManualGame()
        manual.new_game(recording_enabled=True)
        manual.handle_click(1, 3)
        manual.handle_click(3, 3)
        recorded = recorded_game_from_manual_game(manual)
        window = make_window()

        window._on_replay_recorded_game(recorded)

        assert isinstance(window._game, AutomatedGame)
        assert window._game.is_replay_active()
        assert window._autoplay_running
        assert window.refresh_count == 1
        assert len(window.after_calls) == 1

    def test_replay_completion_does_not_show_game_over_dialog(self):
        manual = ManualGame()
        manual.new_game(recording_enabled=True)
        manual.handle_click(1, 3)
        manual.handle_click(3, 3)
        recorded = recorded_game_from_manual_game(manual)
        window = make_window()
        window._on_replay_recorded_game(recorded)
        window._show_game_over = lambda: (_ for _ in ()).throw(AssertionError("no dialog"))

        window._run_autoplay()
        window._run_autoplay()

        assert not window._autoplay_running
        assert window._replay_completed

    def test_replay_does_not_show_game_over_between_events(self):
        manual = ManualGame()
        manual.new_game(recording_enabled=True)
        game_over_grid = [[cell for cell in row] for row in manual.board.grid]
        for r, row in enumerate(game_over_grid):
            for c, cell in enumerate(row):
                if cell != -1:
                    game_over_grid[r][c] = 0
        game_over_grid[3][3] = 1
        restored_grid = [row[:] for row in manual.board.grid]
        recorded = RecordedGame(
            board_type="english",
            size=7,
            moves=[],
            events=[
                {"type": "randomize", "grid": game_over_grid},
                {"type": "randomize", "grid": restored_grid},
            ],
            starting_grid=manual.starting_grid,
            remaining_pegs=manual.peg_count(),
            won=False,
        )
        window = make_window()
        window._on_replay_recorded_game(recorded)
        window._show_game_over = lambda: (_ for _ in ()).throw(AssertionError("no dialog"))

        window._run_autoplay()

        assert window._autoplay_running
        assert not window._replay_completed
        assert len(window.after_calls) == 2

    def test_randomize_is_ignored_after_replay_completes(self):
        manual = ManualGame()
        manual.new_game(recording_enabled=True)
        manual.handle_click(1, 3)
        manual.handle_click(3, 3)
        recorded = recorded_game_from_manual_game(manual)
        window = make_window()
        window._on_replay_recorded_game(recorded)
        window._run_autoplay()
        window._run_autoplay()
        completed_grid = [row[:] for row in window._game.board.grid]
        refreshes_before = window.refresh_count

        window._on_randomize()

        assert window._game.board.grid == completed_grid
        assert window.refresh_count == refreshes_before
