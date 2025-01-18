import tkinter as tk
from tkinter import ttk

from gui.widgets.dropdown_menu import DropdownMenu
from gui.theme.theme_manager import ThemeManager
from gui.widgets.custom_frame import CustomFrame

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("focus app!!")
        self.geometry("600x400")

        self.theme_manager = ThemeManager()

        self.bkgr_frame = CustomFrame(self)
        self.bkgr_frame.pack(fill=tk.BOTH, expand=True)

        self.theme_var = tk.StringVar(value="Default")
        self.dropdown = ttk.Combobox(self, textvariable=self.theme_var, state="readonly")
        self.dropdown["values"] = self.theme_manager.get_all_theme_names()
        self.bkgr_frame.add(self.dropdown, 10, 10)

        self.extra_button = tk.Button(self, text="Extra")
        self.extra_button_var = {"button": self.extra_button, "action": self.extra_button_action}

        self.dropdown.bind("<<ComboboxSelected>>", self.on_dropdown_select)
        self.change_theme("Default")

    def on_dropdown_select(self, event=None):
        selected_theme = self.theme_var.get()
        if selected_theme == "Add Custom Theme":
            new_theme = self.theme_manager.create_custom_theme()
            if new_theme:
                self.update_dropdown_menu()
                self.theme_var.set(new_theme)
                self.change_theme(new_theme)
        else:
            self.change_theme(selected_theme)

    def update_dropdown_menu(self):
        self.dropdown["values"] = self.theme_manager.get_all_theme_names()

    def change_theme(self, theme_name):
        theme_config = self.theme_manager.get_theme_config(theme_name)
        if not theme_config:
            return
        bg_image_path = theme_config["background"]
        self.bkgr_frame.set_background(bg_image_path)

        if theme_config.get("extra_widget"):
            self.extra_button.config(
                text=theme_config.get("extra_button_text", "Extra"),
                command=self.extra_button_action
            )
            self.bkgr_frame.add(self.extra_button, 100, 10)
        else:
            self.extra_button.place_forget()

    def extra_button_action(self):
        print(f"Extra button clicked on theme: {self.theme_var.get()}")