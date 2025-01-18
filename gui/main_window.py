import tkinter as tk
from tkinter import ttk

from gui.theme.theme_manager import ThemeManager
from gui.widgets.custom_frame import CustomFrame
from gui.widgets.tab import TabWidget  

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
        self.bkgr_frame.add(self.dropdown, x=10, y=10)

        self.extra_button = tk.Button(self, text="Extra")
        self.extra_button_var = {"button": self.extra_button, "action": self.extra_button_action}

        self.dropdown.bind("<<ComboboxSelected>>", self.on_dropdown_select)
        self.change_theme("Default")

        self.create_widgets()

    def create_widgets(self):
        tab_widget = TabWidget(self.bkgr_frame)
        self.bkgr_frame.add(tab_widget, x=50, y=50, center_x=True, center_y=True)

        # Frames 
        screen_tab = tk.Frame(tab_widget)
        face_tab = tk.Frame(tab_widget)

        tab_widget.add_tab(screen_tab, "Screen")
        tab_widget.add_tab(face_tab, "Face")

        tab_widget.pack(expand=1, fill="both")

        # Placeholder text, remove later
        screen_label = tk.Label(screen_tab, text="This should show the screen captured")
        face_label = tk.Label(face_tab, text="This should show the face captured")

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