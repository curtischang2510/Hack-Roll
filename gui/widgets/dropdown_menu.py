import tkinter as tk
from tkinter import ttk

class DropdownMenu(tk.Frame):
    def __init__(self, parent, label_text, options=None, callback=None, default=None):
        """

        Args:
            parent (tk.Widget): The parent widget.
            label_text (str): Label text displayed next to the dropdown.
            options (list): A list of options for the dropdown menu.
            callback (function): Function to call when an option is selected.
            default (str): Default selected option.
        """
        super().__init__(parent)
        
        self.callback = callback

        self.label = tk.Label(self, text=label_text)
        self.label.pack(side=tk.TOP, anchor="w", padx=5)

        self.var = tk.StringVar()
        self.dropdown = ttk.Combobox(self, textvariable=self.var, state="readonly")
        self.dropdown.pack(side=tk.LEFT, padx=5)

        if options:
            self.set_options(options, default)

        self.dropdown.bind("<<ComboboxSelected>>", self.on_select)

    def set_options(self, options, default=None):
        """
        Set the options for the dropdown menu and optionally select a default value.

        Args:
            options (list): A list of options for the dropdown menu.
            default (str): Default selected option.
        """
        self.dropdown["values"] = options
        if default and default in options:
            self.var.set(default)
        elif options:
            self.var.set(options[0])

    def on_select(self, event=None):
        """Callback when an option is selected."""
        if self.callback:
            self.callback(self.var.get())

    def get_selected(self):
        """Return the currently selected option."""
        return self.var.get()

    def set_selected(self, value):
        """Set the currently selected option programmatically."""
        if value in self.dropdown["values"]:
            self.var.set(value)