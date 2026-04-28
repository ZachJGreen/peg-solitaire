import tkinter as tk
from tkinter import ttk

class GameControlsView(tk.Frame):
    def __init__(self, parent, on_new_game, on_autoplay=None, on_randomize=None,
                 on_undo=None, on_redo=None, on_show_recorded_games=None):
        super().__init__(parent, background="red")
        self.new_game_button = ttk.Button(self, text="New Game", command=on_new_game)
        self.autoplay_button = ttk.Button(self, text="AutoPlay", command=on_autoplay)
        self.randomize_button = ttk.Button(self, text="Randomize", command=on_randomize)
        self.undo_button = ttk.Button(self, text="Undo", command=on_undo)
        self.redo_button = ttk.Button(self, text="Redo", command=on_redo)
        self.recorded_games_button = ttk.Button(self, text="Recorded Games",
                                                command=on_show_recorded_games)

        self.new_game_button.pack()
        self.autoplay_button.pack()
        self.randomize_button.pack()
        self.undo_button.pack()
        self.redo_button.pack()
        self.recorded_games_button.pack()
