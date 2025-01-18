import tkinter as tk

class CustomButton(tk.Button):
    def __init__(self, parent, text, command=None, color="blue"):
        super().__init__(parent, text=text, command=command, bg=color, fg="white")
