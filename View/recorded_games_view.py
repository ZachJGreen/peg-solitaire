import tkinter as tk
from tkinter import ttk


WIN_COLOR = "lightgreen"
LOSS_COLOR = "#f4b6b6"


def format_move_log(game):
    if not game.moves:
        return "No moves recorded."
    return "\n".join(
        f"{index}. ({fr}, {fc}) -> ({tr}, {tc})"
        for index, (fr, fc, tr, tc) in enumerate(game.moves, start=1)
    )


def format_recorded_game_summary(game, index):
    result = "Won" if game.won else "Lost"
    return (
        f"Game {index}: {result} | "
        f"Moves: {game.move_count} | "
        f"Remaining pegs: {game.remaining_pegs}"
    )


def format_recorded_games(games):
    if not games:
        return "No recorded games this session."
    return "\n".join(
        format_recorded_game_summary(game, index)
        for index, game in enumerate(games, start=1)
    )


class RecordedGameEntry(tk.Frame):
    def __init__(self, parent, game, index, on_replay=None):
        color = WIN_COLOR if game.won else LOSS_COLOR
        super().__init__(parent, background=color, padx=8, pady=8)
        self._game = game
        self._index = index
        self._on_replay = on_replay
        self._moves_visible = False

        header = tk.Frame(self, background=color)
        header.pack(fill=tk.X)
        ttk.Label(header, text=f"Game {index}").pack(side=tk.LEFT)
        ttk.Label(header, text=f"Moves: {game.move_count}").pack(side=tk.LEFT, padx=8)
        ttk.Label(header, text=f"Remaining pegs: {game.remaining_pegs}").pack(side=tk.LEFT)

        button_row = tk.Frame(self, background=color)
        button_row.pack(fill=tk.X, pady=(6, 0))
        self._toggle_button = ttk.Button(button_row, text="Show Moves",
                                         command=self._toggle_moves)
        self._toggle_button.pack(side=tk.LEFT)
        ttk.Button(button_row, text="Replay",
                   command=self._replay).pack(side=tk.RIGHT)

        self._move_log = tk.Text(self, height=min(max(game.move_count, 1), 8),
                                 width=42, wrap=tk.WORD)
        self._move_log.insert(tk.END, format_move_log(game))
        self._move_log.configure(state=tk.DISABLED)

    def _toggle_moves(self):
        if self._moves_visible:
            self._move_log.pack_forget()
            self._toggle_button.configure(text="Show Moves")
            self._moves_visible = False
            return

        self._move_log.pack(fill=tk.X, pady=(6, 0))
        self._toggle_button.configure(text="Hide Moves")
        self._moves_visible = True

    def _replay(self):
        if self._on_replay is not None:
            self._on_replay(self._game)


class RecordedGamesView(tk.Toplevel):
    def __init__(self, parent, games, on_replay=None):
        super().__init__(parent)
        self.title("Recorded Games")

        frame = tk.Frame(self, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Recorded Games").pack(anchor=tk.W)
        if not games:
            ttk.Label(frame, text="No recorded games this session.").pack(anchor=tk.W, pady=8)
            return

        for index, game in enumerate(games, start=1):
            entry = RecordedGameEntry(frame, game, index, on_replay)
            entry.pack(fill=tk.X, pady=5)
