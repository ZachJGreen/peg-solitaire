import tkinter as tk
from View.board_info_view import BoardInfoView
from View.game_controls_view import GameControlsView
from View.settings_view import SettingsView

class MenuView(tk.Frame):
    def __init__(self, parent, on_new_game, on_autoplay=None, on_randomize=None):
        super().__init__(parent, background="blue")

        self.board_info = BoardInfoView(self)
        self.board_info.pack(fill=tk.X)

        self.game_controls = GameControlsView(self, on_new_game, on_autoplay, on_randomize)
        self.game_controls.pack(fill=tk.X)

        self.settings = SettingsView(self)
        self.settings.pack(fill=tk.X)
