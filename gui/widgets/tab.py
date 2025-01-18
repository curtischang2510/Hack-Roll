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

    def resize(self, width, height):
        """Resize the TabWidget and its canvas."""
        self.config(width=width, height=height)
        self.canvas.config(width=width, height=height)
