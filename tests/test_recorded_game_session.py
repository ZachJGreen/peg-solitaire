from Model.game import ManualGame
from Model.recorded_game_session import RecordedGameSession


class TestRecordedGameSession:
    def test_new_session_starts_with_no_recorded_games(self):
        session = RecordedGameSession()

        assert session.games == []

    def test_records_game_snapshot_when_recording_was_enabled(self):
        game = ManualGame()
        game.new_game(board_type="english", size=7, recording_enabled=True)
        game.handle_click(1, 3)
        game.handle_click(3, 3)

        session = RecordedGameSession()
        assert session.add_game(game)

        assert len(session.games) == 1
        recorded = session.games[0]
        assert recorded.board_type == "english"
        assert recorded.size == 7
        assert recorded.moves == [(1, 3, 3, 3)]
        assert recorded.events == [{
            "type": "move",
            "from": (1, 3),
            "to": (3, 3),
        }]
        assert recorded.starting_grid[3][3] == 0
        assert recorded.remaining_pegs == game.peg_count()
        assert not recorded.won
        assert recorded.move_count == 1

    def test_records_randomize_event_with_resulting_grid(self):
        game = ManualGame()
        game.new_game(recording_enabled=True)
        game.randomize()

        session = RecordedGameSession()
        assert session.add_game(game)

        event = session.games[0].events[0]
        assert event["type"] == "randomize"
        assert event["grid"] == game.board.grid

    def test_does_not_record_when_game_recording_was_disabled(self):
        game = ManualGame()
        game.new_game(recording_enabled=False)
        game.handle_click(1, 3)
        game.handle_click(3, 3)

        session = RecordedGameSession()
        assert not session.add_game(game)

        assert session.games == []

    def test_does_not_record_games_with_no_recorded_moves(self):
        game = ManualGame()
        game.new_game(recording_enabled=True)

        session = RecordedGameSession()
        assert not session.add_game(game)

        assert session.games == []

    def test_recorded_snapshot_is_not_mutated_by_later_game_changes(self):
        game = ManualGame()
        game.new_game(recording_enabled=True)
        game.handle_click(1, 3)
        game.handle_click(3, 3)

        session = RecordedGameSession()
        session.add_game(game)
        game.undo_move()

        assert session.games[0].moves == [(1, 3, 3, 3)]
