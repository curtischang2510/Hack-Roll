import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from gui.theme.theme_manager import ThemeManager
from gui.widgets.tab import TabWidget
# from screenshot import VLM
from gui.widgets.timer import TimerWidget

import random
from pygame import mixer

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

        # Will store info about each widget, including new "anchor_bottom_left" flag
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

        try:
            mixer.init()
            print("Mixer initialized successfully.")
        except Exception as e:
            print(f"Error initializing mixer: {e}")

        # Whenever the canvas resizes, attempt to recenter or reposition everything
        self.canvas.bind("<Configure>", self.center_widgets)
        # self.vlm = VLM()

        self.check_periodically()
    
    def check_periodically(self): 
        print("periodically called")
        self.perform_check()

        self.after(5000, self.check_periodically)

    def perform_check(self): 
        print("test")
        theme_name = self.theme_var.get()
        print(theme_name)
        theme_config = self.theme_manager.get_theme_config(theme_name)
        print(theme_config)
        audio_files = theme_config.get("audio", [])
            
        if audio_files:
            random_audio = random.choice(audio_files)
            self.play_audio(random_audio)

        # if not self.vlm.check_laptop_screen():
        #     print("nooooooooo")
        #     theme_name = self.theme_var.get()
        #     theme_config = self.theme_manager.get_theme_config(theme_name)
        #     audio_files = theme_config.get("audio", [])
            
        #     if audio_files:
        #         random_audio = random.choice(audio_files)
        #         self.play_audio(random_audio)
        # else: 
        #     print("yesssss")
        #     pass

    def play_audio(self, audio_path):
            """Plays the given audio file using pygame."""
            try:
                mixer.music.load(audio_path)
                mixer.music.play()
            except Exception as e:
                print(f"Error playing audio: {e}")

    def center_widgets(self, event=None):
        """Center or reposition widgets on the canvas after size changes."""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        for ref in self.widget_references:
            widget = ref["widget"]
            window_id = ref["window_id"]
            x = ref.get("x", 0)
            y = ref.get("y", 0)
            center_x = ref.get("center_x", False)
            center_y = ref.get("center_y", False)
            anchor_bottom_left = ref.get("anchor_bottom_left", False)  # new flag

            # If this widget is our TabWidget, resize it to fill space
            if widget == self.tab_widget:
                tab_width = max(canvas_width - 130, 0)
                tab_height = max(canvas_height - 130, 0)
                widget.resize(tab_width, tab_height)

            # Handle normal center_x/center_y
            if center_x:
                widget.update_idletasks()
                widget_width = widget.winfo_reqwidth()
                x = (canvas_width - widget_width) // 2

            if center_y:
                widget.update_idletasks()
                widget_height = widget.winfo_reqheight()
                y = (canvas_height - widget_height) // 2

            # NEW: if anchor_bottom_left is True, stick the widget to bottom-left
            if anchor_bottom_left:
                widget.update_idletasks()
                widget_width = widget.winfo_reqwidth()
                widget_height = widget.winfo_reqheight()
                # For a small margin from edges, offset by 10px
                x = 10
                y = canvas_height - widget_height - 10

            # Apply updated (x, y) to the widget's position on the canvas
            self.canvas.coords(window_id, x, y)

    def add(self, widget, x=0, y=0, center_x=False, center_y=False, anchor_bottom_left=False):
        """
        Add a widget to the canvas at a given x,y or with certain anchors.
        
        center_x/center_y -> center in canvas 
        anchor_bottom_left -> keep pinned in bottom-left on resize
        """
        window_id = self.canvas.create_window(x, y, anchor=tk.NW, window=widget)
        self.widget_references.append({
            "widget": widget,
            "window_id": window_id,
            "x": x,
            "y": y,
            "center_x": center_x,
            "center_y": center_y,
            "anchor_bottom_left": anchor_bottom_left
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

            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img, tag="image")

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

        # ---------------------------------------------------
        # Create and add the TimerWidget, anchored bottom-left
        # ---------------------------------------------------
        self.timer_widget = TimerWidget(self)
        # Instead of a fixed y=350, just anchor it so it will stay 
        # at bottom-left regardless of window size
        self.add(self.timer_widget, anchor_bottom_left=True)
        # ---------------------------------------------------

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
