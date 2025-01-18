import tkinter as tk
from tkinter import ttk

class TabWidget(ttk.Notebook):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.pack(expand=1, fill="both")
        
        self.tabs = {}
        self.bind("<<NotebookTabChanged>>", self.on_tab_change)
    
    def add_tab(self, frame, title):
        frame.configure(borderwidth=0, relief="flat")
        self.add(frame, text=title)
        self.tabs[title] = frame

    def on_tab_change(self, event):
        selected_tab = event.widget.tab(event.widget.select(), "text")
        print(f"Switched to tab: {selected_tab}")  # For debugging
