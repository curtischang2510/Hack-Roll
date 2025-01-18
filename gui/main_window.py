import tkinter as tk
from gui.widgets.custom_button import CustomButton

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modular Tkinter App")
        self.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        button = CustomButton(self, text="Click Me", command=self.on_button_click)
        button.pack(pady=10)

    def on_button_click(self):
        print("Button clicked!")