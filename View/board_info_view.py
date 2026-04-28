import tkinter as tk
from tkinter import ttk

BOARD_TYPES = ["english", "hexagon", "diamond"]

class BoardInfoView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, background="yellow")

        # Board size entry
        size_row = tk.Frame(self, background="yellow")
        size_row.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(size_row, text="Board Size:", background="yellow").pack(side=tk.LEFT)
        self._size_var = tk.StringVar(value="7")
        ttk.Entry(size_row, textvariable=self._size_var, width=5).pack(side=tk.LEFT, padx=4)

        # Board type radio buttons
        type_row = tk.Frame(self, background="yellow")
        type_row.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(type_row, text="Board Type:", background="yellow").pack(anchor=tk.W)
        self._type_var = tk.StringVar(value="english")
        for t in BOARD_TYPES:
            ttk.Radiobutton(type_row, text=t.capitalize(),
                            variable=self._type_var, value=t).pack(anchor=tk.W)

        record_row = tk.Frame(self, background="yellow")
        record_row.pack(fill=tk.X, padx=5, pady=2)
        self._recording_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(record_row, text="Record Game",
                        variable=self._recording_var).pack(anchor=tk.W)

    def get_type(self):
        return self._type_var.get()

    def get_size(self):
        try:
            return int(self._size_var.get())
        except ValueError:
            return None

    def is_recording_enabled(self):
        return self._recording_var.get()

    def set_recording_enabled(self, enabled):
        self._recording_var.set(bool(enabled))

    def update(self, board_type, size):
        self._type_var.set(board_type)
        self._size_var.set(str(size))
