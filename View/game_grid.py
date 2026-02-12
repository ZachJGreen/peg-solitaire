import tkinter as tk
class game_grid(tk.Frame):
    grid_buttons = []
    def __init__(self, parent, grid_size):
        super().__init__(parent)
        for row in range(grid_size):
            row_list = []
            for col in range(grid_size):
                cell = tk.Button(self, width=2, height=2, command=lambda r=row, c=col: onclick(r, c))
                row_list.append(cell)
                cell.grid(row=row, column=col)
            self.grid_buttons.append(row_list)

# root = tk.Tk()
# root.title("game_grid.py")
# root.geometry("1280x720")

# grid = game_grid(root, 10)
# grid.pack()
# root.mainloop()