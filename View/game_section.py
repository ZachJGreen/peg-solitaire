import tkinter as tk
from tkinter import Tk
from tkinter import ttk
from counter_view import CounterView
from game_grid import GameGrid
class GameSection(tk.Frame):
    def __init__(self, parent, grid_size):
        super().__init__(parent)

        # Add Counter Box
        counter_box = CounterView(self)
        counter_box.pack()

        # Add Game Grid
        grid = GameGrid(self, grid_size)
        grid.pack(pady=50)

