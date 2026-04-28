import inspect

from Model.game import ManualGame
from View.game_controls_view import GameControlsView
from View.main_window import MainWindow
from View.menu_view import MenuView


def make_window():
    window = MainWindow.__new__(MainWindow)
    window._game = ManualGame()
    window._autoplay_running = False
    window.refresh_count = 0

    def refresh():
        window.refresh_count += 1

    window._refresh = refresh
    return window


class TestUndoRedoControls:
    def test_game_controls_accept_undo_and_redo_callbacks(self):
        signature = inspect.signature(GameControlsView.__init__)

        assert "on_undo" in signature.parameters
        assert "on_redo" in signature.parameters

    def test_game_controls_wire_undo_and_redo_buttons(self):
        source = inspect.getsource(GameControlsView)

        assert "command=on_undo" in source
        assert "command=on_redo" in source

    def test_menu_view_passes_undo_and_redo_callbacks(self):
        signature = inspect.signature(MenuView.__init__)
        source = inspect.getsource(MenuView)

        assert "on_undo" in signature.parameters
        assert "on_redo" in signature.parameters
        assert "on_undo" in source
        assert "on_redo" in source

    def test_undo_refreshes_after_successful_undo(self):
        window = make_window()
        window._game.new_game()
        window._game.handle_click(1, 3)
        window._game.handle_click(3, 3)

        window._on_undo()

        assert window._game.moves_made == 0
        assert window.refresh_count == 1

    def test_undo_without_move_does_not_refresh(self):
        window = make_window()
        window._game.new_game()

        window._on_undo()

        assert window.refresh_count == 0

    def test_redo_refreshes_after_successful_redo(self):
        window = make_window()
        window._game.new_game()
        window._game.handle_click(1, 3)
        window._game.handle_click(3, 3)
        window._game.undo_move()

        window._on_redo()

        assert window._game.moves_made == 1
        assert window.refresh_count == 1

    def test_redo_without_undone_move_does_not_refresh(self):
        window = make_window()
        window._game.new_game()

        window._on_redo()

        assert window.refresh_count == 0
