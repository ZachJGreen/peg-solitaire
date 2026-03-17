import tkinter as tk
from tkinter import ttk

class CounterView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, background="brown", width=500, height=75)
        self.pack_propagate(False)

        inner_frame = tk.Frame(self, background="gray")
        inner_frame.pack(fill=tk.X, expand=True)

        self._moves_label = ttk.Label(inner_frame, text="Moves Made: 0", background="yellow")
        self._pegs_label = ttk.Label(inner_frame, text="Pegs Remaining: 0", background="lightblue")

        self._moves_label.pack(fill=tk.X)
        self._pegs_label.pack(fill=tk.X)

    def update(self, moves, pegs):
        self._moves_label.config(text=f"Moves Made: {moves}")
        self._pegs_label.config(text=f"Pegs Remaining: {pegs}")
