import tkinter as tk
from tkinter import ttk

class BoardInfoView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, background="yellow")
        self.board_type_label = ttk.Label(self, text="Board Type: ---")
        self.board_size_label = ttk.Label(self, text="Board Size: ---")

        self.board_type_label.pack()
        self.board_size_label.pack()

