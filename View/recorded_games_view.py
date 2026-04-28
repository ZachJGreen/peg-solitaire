import tkinter as tk
from tkinter import ttk


def format_recorded_games(games):
    if not games:
        return "No recorded games this session."

    sections = []
    for index, game in enumerate(games, start=1):
        lines = [
            f"Game {index}: {game.board_type.capitalize()} board, size {game.size}",
        ]
        for move_index, (fr, fc, tr, tc) in enumerate(game.moves, start=1):
            lines.append(f"{move_index}. ({fr}, {fc}) -> ({tr}, {tc})")
        sections.append("\n".join(lines))
    return "\n\n".join(sections)


class RecordedGamesView(tk.Toplevel):
    def __init__(self, parent, games):
        super().__init__(parent)
        self.title("Recorded Games")

        frame = tk.Frame(self, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Recorded Games").pack(anchor=tk.W)
        text = tk.Text(frame, width=45, height=18, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, pady=5)
        text.insert(tk.END, format_recorded_games(games))
        text.configure(state=tk.DISABLED)
