import tkinter as tk
from Model.board import NOT_PLAYED, OPEN_SPACE, PEG

CELL_COLORS = {NOT_PLAYED: "gray", OPEN_SPACE: "white", PEG: "sienna"}

class GameGrid(tk.Frame):
    def __init__(self, parent, on_click):
        super().__init__(parent)
        self._on_click = on_click

    def update(self, board_grid, selected=None):
        for widget in self.winfo_children():
            widget.destroy()
        for r, row in enumerate(board_grid):
            for c, cell in enumerate(row):
                if cell == NOT_PLAYED:
                    btn = tk.Label(self, width=3, height=1, bg="gray", relief="flat")
                else:
                    color = "yellow" if selected == (r, c) else CELL_COLORS[cell]
                    btn = tk.Button(self, width=3, height=1, bg=color,
                                    command=lambda r=r, c=c: self._on_click(r, c))
                btn.grid(row=r, column=c)
