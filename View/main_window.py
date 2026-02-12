# Menu: ~33%, Game: ~67%
from tkinter import Frame
from tkinter import PanedWindow
from tkinter import ttk
import tkinter as tk
from game_section import game_section
class main_window(Frame):
    MENU_WIDTH_RATIO = 0.33
    GAME_WIDTH_RATIO = 0.67
    def __init__(self, parent, dimX, dimY):
        super().__init__(parent, background="yellow")

        panes = PanedWindow(self, orient=tk.HORIZONTAL, background="blue")
        panes.pack(fill=tk.BOTH, expand=True, pady=10)

        menu_frame = Frame(panes, background="lightgreen", width=(dimX * self.MENU_WIDTH_RATIO), pady=10)
        menu_frame.pack(fill=tk.BOTH)

        game_frame = Frame(panes, background="red", width=(dimX * self.GAME_WIDTH_RATIO), pady=10)
        game_frame.pack(fill=tk.BOTH)

        panes.add(menu_frame)
        panes.add(game_frame)

        game = game_section(game_frame, 10)
        game.pack()
dimension_x = 1280
dimension_y = 720

root = tk.Tk()
root.title("main_window.py")
root.geometry("1280x720")
root.main_window = main_window(root, dimension_x, dimension_y)
root.main_window.pack(fill=tk.BOTH, expand=True)
root.mainloop()