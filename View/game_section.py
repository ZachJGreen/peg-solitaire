import tkinter as tk
from tkinter import Tk
from tkinter import ttk
from counter_view import counter_view
from game_grid import game_grid
class game_section(tk.Frame):
    def __init__(self, parent, grid_size):
        super().__init__(parent)

        # Add Counter Box
        counter_box = counter_view(self)
        counter_box.pack()

        # Add Game Grid
        grid = game_grid(self, grid_size)
        grid.pack(pady=50)

