import tkinter as tk
from tkinter import Tk
from tkinter import ttk
# Pegs Remaining Counter
# Moves Made Counter

class counter_view(tk.Frame):

    def __init__(self, parent):
        self.moves_made = 0
        self.pegs_remaining = 50
        super().__init__(parent, background="brown", width=500, height=75)
        self.pack_propagate(False)

        inner_frame = tk.Frame(self, background="gray")
        inner_frame.pack(fill=tk.X,expand=True)

        moves_counter = ttk.Label(inner_frame, text=f"Moves Made: {self.moves_made}", background="yellow")
        pegs_counter = ttk.Label(inner_frame, text=f"Pegs Remaining: {self.pegs_remaining}", background="lightblue")

        moves_counter.pack(fill=tk.X)
        pegs_counter.pack(fill=tk.X)



# root = Tk()
# root.title("counter_view.py")
# root.geometry("800x300")
# box = counter_view(root)
# box.pack(fill=tk.NONE, expand=True)
# root.mainloop()