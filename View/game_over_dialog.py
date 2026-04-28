import tkinter as tk
from tkinter import ttk


GAME_OVER_RANDOMIZE_LIMIT = 3


class GameOverDialog(tk.Toplevel):
    def __init__(self, parent, message, on_randomize, on_new_game, on_close=None,
                 randomizes_remaining=GAME_OVER_RANDOMIZE_LIMIT):
        super().__init__(parent)
        self.title("Game Over")
        self._on_randomize = on_randomize
        self._on_new_game = on_new_game
        self._on_close = on_close
        self._closed_after_recovery = False

        frame = tk.Frame(self, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=message).pack(anchor=tk.W)
        self._remaining_var = tk.StringVar()
        ttk.Label(frame, textvariable=self._remaining_var).pack(anchor=tk.W, pady=(6, 0))

        button_row = tk.Frame(frame)
        button_row.pack(fill=tk.X, pady=(10, 0))
        self._randomize_button = ttk.Button(button_row, text="Randomize",
                                            command=self._randomize)
        self._randomize_button.pack(side=tk.LEFT)
        ttk.Button(button_row, text="New Game",
                   command=self._new_game).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_row, text="Close",
                   command=self._close).pack(side=tk.LEFT)

        self.protocol("WM_DELETE_WINDOW", self._close)
        self.update_randomizes_remaining(randomizes_remaining)

    def update_randomizes_remaining(self, remaining):
        self._remaining_var.set(f"Randomizes remaining: {remaining}")
        if remaining <= 0:
            self._randomize_button.configure(state=tk.DISABLED)

    def _randomize(self):
        recovered, remaining = self._on_randomize()
        if recovered:
            self._closed_after_recovery = True
            self.destroy()
            return
        self.update_randomizes_remaining(remaining)

    def _new_game(self):
        if self._on_close is not None:
            self._on_close()
        self.destroy()
        self._on_new_game()

    def _close(self):
        if not self._closed_after_recovery and self._on_close is not None:
            self._on_close()
        self.destroy()
