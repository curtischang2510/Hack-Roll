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
        # self.tab_container = tk.Frame(self.canvas)
        # self.tab_window = self.canvas.create_window(
        #     0, 0, anchor=tk.NW, window=self.tab_container
        # )
        self.change_theme("Default")

        # self.create_widgets()
    
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

            # Clear and redraw canvas
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

            # Re-add all widgets
            for widget_ref in self.widget_references:
                widget = widget_ref["widget"]
                x = widget_ref["x"]
                y = widget_ref["y"]
                center_x = widget_ref.get("center_x", False)
                center_y = widget_ref.get("center_y", False)
                
                final_x = x
                final_y = y
                
                if center_x:
                    final_x = (width - widget.winfo_width()) // 2 + x
                
                if center_y:
                    final_y = (height - widget.winfo_height()) // 2 + y
                    
                self.canvas.create_window(final_x, final_y, anchor=tk.NW, window=widget)

    def create_widgets(self):

        # Create TabWidget inside the container frame
        tab_widget = TabWidget(self.tab_container)

        # Create tabs
        screen_tab = tk.Frame(tab_widget)
        face_tab = tk.Frame(tab_widget)

        # Add tabs to the TabWidget
        tab_widget.add_tab(screen_tab, "Screen")
        tab_widget.add_tab(face_tab, "Face")

        # Pack the TabWidget inside the container frame
        tab_widget.pack(expand=True, fill=tk.BOTH)

        # Add placeholder labels to the tabs
        screen_label = tk.Label(screen_tab, text="This should show the screen captured")
        screen_label.pack(expand=True, fill=tk.BOTH)
        face_label = tk.Label(face_tab, text="This should show the face captured")
        face_label.pack(expand=True, fill=tk.BOTH)

        # Add the container frame (with the TabWidget) to the canvas
        # self.tab_window = self.canvas.create_window(
        #     0, 0, anchor=tk.NW, window=self.tab_container
        # )

        # self.center_tabs()

    def center_tabs(self):
        """Center the TabWidget in the canvas."""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        self.tab_container.update_idletasks()  # Ensure correct size calculations
        tab_width = self.tab_container.winfo_width()
        tab_height = self.tab_container.winfo_height()

        # Calculate the centered position
        x = (canvas_width - tab_width) // 2
        y = (canvas_height - tab_height) // 2

        # Update the position of the container frame
        self.canvas.coords(self.tab_window, x, y)

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