import tkinter as tk
class GameGrid(tk.Frame):

    def __init__(self, parent, grid_size):
        super().__init__(parent)
        grid_buttons = []
        for row in range(grid_size):
            row_list = []
            for col in range(grid_size):
                cell = tk.Button(self, width=2, height=2, command=lambda r=row, c=col: onclick(r, c))
                row_list.append(cell)
                cell.grid(row=row, column=col)
            grid_buttons.append(row_list)