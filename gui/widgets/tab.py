# import tkinter as tk
# from tkinter import ttk

# class TabWidget(ttk.Notebook):
#     def __init__(self, parent, *args, **kwargs):
#         super().__init__(parent, *args, **kwargs)

#         self.pack(expand=1, fill="both")
        
#         self.tabs = {}
#         self.bind("<<NotebookTabChanged>>", self.on_tab_change)
    
#     def add_tab(self, frame, title):
#         frame.configure(borderwidth=0, relief="flat")
#         self.add(frame, text=title)
#         self.tabs[title] = frame

#     def on_tab_change(self, event):
#         selected_tab = event.widget.tab(event.widget.select(), "text")
#         print(f"Switched to tab: {selected_tab}")  # For debugging


import tkinter as tk

class TabWidget(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.tabs = {}
        self.active_tab = None

        self.tab_buttons_frame = tk.Frame(self)
        self.tab_buttons_frame.pack(side=tk.TOP, fill=tk.X)

    def add_tab(self, frame, title):
        """Add a new tab to the widget."""
        # Hide the frame initially
        frame.place_forget()

        # Store the frame and its title
        self.tabs[title] = frame

        # Create a button for the tab
        button = tk.Button(self.tab_buttons_frame, text=title, command=lambda: self.switch_to_tab(title))
        button.pack(side=tk.LEFT)

        # Switch to the first tab added by default
        if self.active_tab is None:
            self.switch_to_tab(title)

    def switch_to_tab(self, title):
        """Switch to a specific tab by title."""
        if title not in self.tabs:
            return

        # Hide the currently active tab
        if self.active_tab:
            self.tabs[self.active_tab].place_forget()

        # Show the selected tab
        new_tab = self.tabs[title]
        new_tab.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.active_tab = title
