# Menu: ~33%, Game: ~67%
from tkinter import Frame, PanedWindow, messagebox
import tkinter as tk
from Model.game import ManualGame, AutomatedGame
from Model.recorded_game_session import RecordedGameSession
from View.game_over_dialog import GAME_OVER_RANDOMIZE_LIMIT, GameOverDialog
from View.game_section import GameSection
from View.menu_view import MenuView
from View.recorded_games_view import RecordedGamesView

AUTOPLAY_DELAY_MS = 300

class MainWindow(Frame):
    MENU_WIDTH_RATIO = 0.33
    GAME_WIDTH_RATIO = 0.67

    def __init__(self, parent, dimX, dimY):
        super().__init__(parent, background="yellow")
        self._game = ManualGame()
        self._autoplay_running = False
        self._recorded_games = RecordedGameSession()
        self._current_game_recorded = False
        self._game_over_randomizes_remaining = GAME_OVER_RANDOMIZE_LIMIT
        self._replay_completed = False

        panes = PanedWindow(self, orient=tk.HORIZONTAL, background="blue")
        panes.pack(fill=tk.BOTH, expand=True, pady=10)

        menu_frame = Frame(panes, background="lightgreen", width=(dimX * self.MENU_WIDTH_RATIO), pady=10)
        menu_frame.pack(fill=tk.BOTH)

        game_frame = Frame(panes, background="red", width=(dimX * self.GAME_WIDTH_RATIO), pady=10)
        game_frame.pack(fill=tk.BOTH)

        panes.add(menu_frame)
        panes.add(game_frame)

        self._menu = MenuView(menu_frame,
                              on_new_game=self._on_new_game,
                              on_autoplay=self._on_autoplay,
                              on_randomize=self._on_randomize,
                              on_undo=self._on_undo,
                              on_redo=self._on_redo,
                              on_show_recorded_games=self._on_show_recorded_games)
        self._menu.pack()

        self._game_section = GameSection(game_frame, on_cell_click=self._on_cell_click)
        self._game_section.pack()

    def _on_new_game(self):
        if self._game.board is not None and self._game.moves_made > 0:
            if not messagebox.askyesno("New Game", "A game is in progress. Start a new game?"):
                return
        self._start_new_game()

    def _start_new_game(self):
        self._autoplay_running = False
        board_type = self._menu.board_info.get_type()
        size = self._menu.board_info.get_size()
        if size is None or size < 3:
            messagebox.showerror("Invalid Size", "Board size must be an integer >= 3.")
            return
        recording_enabled = self._menu.board_info.is_recording_enabled()
        self._record_current_game()
        self._game = ManualGame()
        self._game.new_game(board_type, size, recording_enabled)
        self._current_game_recorded = False
        self._game_over_randomizes_remaining = GAME_OVER_RANDOMIZE_LIMIT
        self._replay_completed = False
        self._refresh()

    def _on_cell_click(self, r, c):
        if not isinstance(self._game, ManualGame):
            return
        self._game.handle_click(r, c)
        self._refresh()
        if self._game.is_game_over():
            self._show_game_over()

    def _on_autoplay(self):
        if self._game.board is None:
            messagebox.showinfo("No Game", "Please start a new game first.")
            return
        # Transfer current board state to an AutomatedGame instance
        automated = AutomatedGame()
        automated.board = self._game.board
        automated.moves_made = self._game.moves_made
        automated.history = list(self._game.history)
        automated.redo_history = list(self._game.redo_history)
        automated.recording_enabled = self._game.recording_enabled
        automated.recorded_moves = list(self._game.recorded_moves)
        automated.recorded_events = list(self._game.recorded_events)
        automated.starting_grid = [row[:] for row in self._game.starting_grid]
        self._game = automated
        self._autoplay_running = True
        self._replay_completed = False
        self._run_autoplay()

    def _run_autoplay(self):
        if not self._autoplay_running:
            return
        moved = self._game.make_auto_move()
        self._refresh()
        if isinstance(self._game, AutomatedGame) and self._game.is_replay_active():
            if not moved:
                self._autoplay_running = False
                self._replay_completed = True
            else:
                self.after(AUTOPLAY_DELAY_MS, self._run_autoplay)
            return
        if not moved or self._game.is_game_over():
            self._autoplay_running = False
            self._show_game_over()
        else:
            self.after(AUTOPLAY_DELAY_MS, self._run_autoplay)

    def _on_randomize(self):
        if self._game.board is None:
            messagebox.showinfo("No Game", "Please start a new game first.")
            return
        if getattr(self, "_replay_completed", False):
            return
        self._game.randomize()
        self._refresh()

    def _on_undo(self):
        self._autoplay_running = False
        if self._game.undo_move():
            if hasattr(self._game, "selected"):
                self._game.selected = None
            self._refresh()

    def _on_redo(self):
        self._autoplay_running = False
        if self._game.redo_move():
            if hasattr(self._game, "selected"):
                self._game.selected = None
            self._refresh()

    def _record_current_game(self):
        if not hasattr(self, "_recorded_games"):
            self._recorded_games = RecordedGameSession()
        if not hasattr(self, "_current_game_recorded"):
            self._current_game_recorded = False
        if self._current_game_recorded:
            return False
        recorded = self._recorded_games.add_game(self._game)
        if recorded:
            self._current_game_recorded = True
        return recorded

    def _on_show_recorded_games(self):
        if not hasattr(self, "_recorded_games"):
            self._recorded_games = RecordedGameSession()
        RecordedGamesView(self, self._recorded_games.games, self._on_replay_recorded_game)

    def _on_replay_recorded_game(self, recorded_game):
        self._autoplay_running = False
        replay = AutomatedGame()
        replay.load_replay(recorded_game)
        self._game = replay
        self._game_over_randomizes_remaining = GAME_OVER_RANDOMIZE_LIMIT
        self._replay_completed = False
        self._refresh()
        self._autoplay_running = True
        self.after(AUTOPLAY_DELAY_MS, self._run_autoplay)

    def _try_game_over_randomize(self):
        if self._game_over_randomizes_remaining <= 0:
            return False, 0

        self._game_over_randomizes_remaining -= 1
        self._game.randomize()
        self._refresh()
        recovered = not self._game.is_game_over()
        if recovered:
            self._game_over_randomizes_remaining = GAME_OVER_RANDOMIZE_LIMIT
            if isinstance(self._game, AutomatedGame):
                self._autoplay_running = True
                self.after(AUTOPLAY_DELAY_MS, self._run_autoplay)
        return recovered, self._game_over_randomizes_remaining

    def _show_game_over(self):
        pegs = self._game.peg_count()
        msg = "You win!" if pegs == 1 else f"No moves left. {pegs} pegs remaining."
        GameOverDialog(self, msg, self._try_game_over_randomize,
                       self._start_new_game, self._record_current_game,
                       self._game_over_randomizes_remaining)

    def _refresh(self):
        if self._game.board is None:
            return
        selected = getattr(self._game, 'selected', None)
        self._game_section.game_grid.update(self._game.board.grid, selected)
        self._game_section.counter_view.update(self._game.moves_made, self._game.peg_count())
