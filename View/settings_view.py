import tkinter as tk
from tkinter import ttk

class SettingsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, background="green")

        settings_button = ttk.Button(self, text="Settings", command=None)
        instructions_button = ttk.Button(self, text="How to Play", command=None)

        settings_button.pack()
        instructions_button.pack()