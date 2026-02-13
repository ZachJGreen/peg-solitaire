# Menu: ~33%, Game: ~67%
from tkinter import Frame
from tkinter import PanedWindow
from tkinter import ttk
import tkinter as tk
from View.game_section import GameSection
from View.menu_view import MenuView

class MainWindow(Frame):
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

        game = GameSection(game_frame, 10)
        game.pack()

        menu = MenuView(menu_frame)
        menu.pack()
