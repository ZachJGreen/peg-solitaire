import tkinter as tk
from View.counter_view import CounterView
from View.game_grid import GameGrid

class GameSection(tk.Frame):
    def __init__(self, parent, on_cell_click):
        super().__init__(parent)

        self.counter_view = CounterView(self)
        self.counter_view.pack()

        self.game_grid = GameGrid(self, on_cell_click)
        self.game_grid.pack(pady=50)
