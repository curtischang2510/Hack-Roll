import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from gui.theme.theme_manager import ThemeManager
from gui.widgets.tab import TabWidget  

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
    
    def add(self, widget, x=0, y=0, center_x=False, center_y=False):
        """Add a widget to the canvas."""
        self.widget_references.append({"widget": widget, "x": x, "y": y})
        self.canvas.create_window(x, y, anchor=tk.NW, window=widget)

    def resize_window(self, event=None):
        """Handle window resize events."""
        if not self.original_img:
            return

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width > 0 and height > 0:
            resized_img = self.original_img.resize((width, height), Image.Resampling.LANCZOS)
            self.img = ImageTk.PhotoImage(resized_img)

            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img, tag="image")

        if not hasattr(self, "widgets_created"):
            self.create_widgets()
            self.widgets_created = True

    def create_widgets(self):
        self.tab_widget = TabWidget(self)

        self.add(self.tab_widget, x=0, y=50, center_x=True)

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
            self.theme_manager.create_custom_theme(self)
            self.update_dropdown_menu()
        else:
            self.change_theme(selected_theme)

    def update_dropdown_menu(self):
        self.dropdown["values"] = self.theme_manager.get_all_theme_names()
        print(f"Dropdown updated: {self.dropdown['values']}")

    def change_theme(self, theme_name):
        theme_config = self.theme_manager.get_theme_config(theme_name)
        print(f"Applying theme: {theme_name}, Config: {theme_config}")
        if not theme_config:
            return

        # Remove any existing background image
        self.canvas.delete("image")
        self.original_img = None

        # Apply background color
        bg_color = theme_config.get("color")
        if bg_color:
            print(f"Existing theme color: {bg_color}")
            self.configure(bg=bg_color)  
            self.canvas.configure(bg=bg_color)  # Ensure the canvas matches the background
        else:
            print("No theme color found.")
            self.configure(bg="#FFFFFF")  # Default background color (white)
            self.canvas.configure(bg="#FFFFFF")

        # Apply background image
        bg_image_path = theme_config.get("image")
        if bg_image_path:
            try:
                self.original_img = Image.open(bg_image_path)
                self.resize_window()  # Resize the window with the new image
            except Exception as e:
                print(f"Error loading image: {e}")
                self.original_img = None  # Clear any failed image load
        else:
            print("No theme image found.")

        # If no color and no image, reset to default canvas
        if not bg_color and not bg_image_path:
            print("Reverting to default canvas.")
            self.configure(bg="#FFFFFF")
            self.canvas.configure(bg="#FFFFFF")

    def extra_button_action(self):
        print(f"Extra button clicked on theme: {self.theme_var.get()}")
