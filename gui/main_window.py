import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from gui.theme.theme_manager import ThemeManager
from gui.widgets.tab import TabWidget
from screenshot import VLM

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("focus app!!")
        self.geometry("600x400")

        self.theme_manager = ThemeManager()

        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.original_img = None
        self.img = None

        self.widget_references = []

        self.bind("<Configure>", self.resize_window)

        self.theme_var = tk.StringVar(value="Default")
        self.dropdown = ttk.Combobox(self, textvariable=self.theme_var, state="readonly")
        self.dropdown["values"] = self.theme_manager.get_all_theme_names()
        self.add(self.dropdown, x=10, y=10)

        self.extra_button = tk.Button(self, text="Extra")
        self.extra_button_var = {"button": self.extra_button, "action": self.extra_button_action}

        self.dropdown.bind("<<ComboboxSelected>>", self.on_dropdown_select)
        self.change_theme("Default")

        self.widgets_created = False

        self.canvas.bind("<Configure>", self.center_widgets)
        self.vlm = VLM()

        self.check_periodically()
    
    def check_periodically(self): 
        print("periodically called")
        self.perform_check()

        self.after(5000, self.check_periodically)

    def perform_check(self): 
        if not self.vlm.check_laptop_screen():
            print("nooooooooo")
            pass
        else: 
            print("yesssss")
            pass

    def center_widgets(self, event=None):
        """Center all widgets on the canvas after size changes."""

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        for ref in self.widget_references:
            widget = ref["widget"]
            window_id = ref["window_id"]
            x = ref.get("x", 0)
            y = ref.get("y", 0)
            center_x = ref.get("center_x", False)
            center_y = ref.get("center_y", False)

            if widget == self.tab_widget:
                tab_width = max(canvas_width - 120, 0)
                tab_height = max(canvas_height - 120, 0)
                widget.resize(tab_width, tab_height) 

            if center_x:
                widget.update_idletasks()
                widget_width = widget.winfo_reqwidth()
                x = (canvas_width - widget_width) // 2
            if center_y:
                widget.update_idletasks()
                widget_height = widget.winfo_reqheight()
                y = (canvas_height - widget_height) // 2
            self.canvas.coords(window_id, x, y)

    def add(self, widget, x=0, y=0, center_x=False, center_y=False):
        """Add a widget to the canvas."""
        window_id = self.canvas.create_window(x, y, anchor=tk.NW, window=widget)
        self.widget_references.append({
            "widget": widget,
            "window_id": window_id,
            "x": x,
            "y": y,
            "center_x": center_x,
            "center_y": center_y,
        })

    def resize_window(self, event=None):
        """Handle window resize events."""
        if not self.original_img:
            return

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width > 0 and height > 0:
            resized_img = self.original_img.resize((width, height), Image.Resampling.LANCZOS)
            self.img = ImageTk.PhotoImage(resized_img)

            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

        if not hasattr(self, "widgets_created"):
            self.create_widgets()

    def create_widgets(self):
        self.widgets_created = True
        self.tab_widget = TabWidget(self)
        self.add(self.tab_widget, center_x=True, center_y=True)

        screen_tab = tk.Frame(self.tab_widget.canvas, bg="lightblue")
        face_tab = tk.Frame(self.tab_widget.canvas, bg="lightgreen")

        self.tab_widget.add_tab(screen_tab, "Screen")
        self.tab_widget.add_tab(face_tab, "Face")

        screen_label = tk.Label(screen_tab, text="This should show the screen captured")
        screen_label.pack(expand=True, fill=tk.BOTH)
        face_label = tk.Label(face_tab, text="This should show the face captured")
        face_label.pack(expand=True, fill=tk.BOTH)

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
        self.original_img = Image.open(bg_image_path)
        self.resize_window()

        if theme_config.get("extra_widget"):
            self.extra_button.config(
                text=theme_config.get("extra_button_text", "Extra"),
                command=self.extra_button_action
            )
        else:
            self.extra_button.place_forget()

    def extra_button_action(self):
        print(f"Extra button clicked on theme: {self.theme_var.get()}")