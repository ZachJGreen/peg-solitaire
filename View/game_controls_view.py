import tkinter as tk
from tkinter import ttk

class GameControlsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, background="red")
        self.new_game_button = ttk.Button(self, text="New Game", command=None)
        self.autoplay_button = ttk.Button(self, text="AutoPlay", command=None)
        self.undo_button = ttk.Button(self, text="Undo", command=None)
        self.redo_button = ttk.Button(self, text="Redo", command=None)

        self.new_game_button.pack()
        self.autoplay_button.pack()
        self.undo_button.pack()
        self.redo_button.pack()
