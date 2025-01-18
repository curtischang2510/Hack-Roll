import tkinter as tk
from gui.widgets.custom_button import CustomButton
from gui.widgets.tab import TabWidget  

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modular Tkinter App")
        self.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        tab_widget = TabWidget(self)

        # Frames 
        screen_tab = tk.Frame(tab_widget)
        face_tab = tk.Frame(tab_widget)

        tab_widget.add_tab(screen_tab, "Screen")
        tab_widget.add_tab(face_tab, "Face")

        tab_widget.pack(expand=1, fill="both")

        # Placeholder text, remove later
        screen_label = tk.Label(screen_tab, text="This should show the screen captured")
        face_label = tk.Label(face_tab, text="This should show the face captured")

    def on_button_click(self):
        print("Button clicked!")

