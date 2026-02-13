from tkinter import Tk
from tkinter import ttk
import tkinter as tk
from View import MainWindow
class App(Tk):
    _dimension_x = 1280
    _dimension_y = 720
    dimensions = f"{str(_dimension_x)}x{str(_dimension_y)}"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("blah")
        self.geometry(self.dimensions)

        self.MainWindow = MainWindow(self, self._dimension_x, self._dimension_y)
        self.MainWindow.pack(fill=tk.BOTH, expand=True)
       

    def on_button_click(self):
        self.label.config(text="guh")

if __name__ == "__main__":
    app = App()
    app.mainloop()