import inspect

from View.board_info_view import BoardInfoView


class TestBoardInfoRecordingOption:
    def test_board_info_view_exposes_recording_getter(self):
        assert hasattr(BoardInfoView, "is_recording_enabled")

    def test_board_info_view_exposes_recording_setter(self):
        assert hasattr(BoardInfoView, "set_recording_enabled")

    def test_board_info_view_adds_recording_checkbox(self):
        source = inspect.getsource(BoardInfoView)

        assert "BooleanVar(value=True)" in source
        assert "ttk.Checkbutton" in source
        assert "Record Game" in source
