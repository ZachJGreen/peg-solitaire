from tkinter import Tk
from tkinter import ttk
import tkinter as tk
from View.main_window import main_window
class App(Tk):
    _dimension_x = 1280
    _dimension_y = 720
    dimensions = f"{str(_dimension_x)}x{str(_dimension_y)}"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("blah")
        self.geometry(self.dimensions)

        self.main_window = main_window(self, self._dimension_x, self._dimension_y)
        self.main_window.pack(fill=tk.BOTH, expand=True)
       

    def on_button_click(self):
        self.label.config(text="guh")

if __name__ == "__main__":
    app = App()
    app.mainloop()