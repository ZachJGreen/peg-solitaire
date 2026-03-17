# Menu: ~33%, Game: ~67%
from tkinter import Frame, PanedWindow, messagebox
import tkinter as tk
from Model.game import Game
from View.game_section import GameSection
from View.menu_view import MenuView

class MainWindow(Frame):
    MENU_WIDTH_RATIO = 0.33
    GAME_WIDTH_RATIO = 0.67

    def __init__(self, parent, dimX, dimY):
        super().__init__(parent, background="yellow")
        self._game = Game()

        panes = PanedWindow(self, orient=tk.HORIZONTAL, background="blue")
        panes.pack(fill=tk.BOTH, expand=True, pady=10)

        menu_frame = Frame(panes, background="lightgreen", width=(dimX * self.MENU_WIDTH_RATIO), pady=10)
        menu_frame.pack(fill=tk.BOTH)

        game_frame = Frame(panes, background="red", width=(dimX * self.GAME_WIDTH_RATIO), pady=10)
        game_frame.pack(fill=tk.BOTH)

        panes.add(menu_frame)
        panes.add(game_frame)

        self._menu = MenuView(menu_frame, on_new_game=self._on_new_game)
        self._menu.pack()

        self._game_section = GameSection(game_frame, on_cell_click=self._on_cell_click)
        self._game_section.pack()

    def _on_new_game(self):
        self._game.new_game()
        self._menu.board_info.update("English", 7)
        self._refresh()

    def _on_cell_click(self, r, c):
        self._game.handle_click(r, c)
        self._refresh()
        if self._game.is_game_over():
            pegs = self._game.peg_count()
            msg = "You win!" if pegs == 1 else f"No moves left. {pegs} pegs remaining."
            messagebox.showinfo("Game Over", msg)

    def _refresh(self):
        self._game_section.game_grid.update(self._game.board.grid, self._game.selected)
        self._game_section.counter_view.update(self._game.moves_made, self._game.peg_count())
