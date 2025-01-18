import os
import json
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
import pysound

class ThemeManager:
    def __init__(self, custom_themes_file="custom_themes.json"):
        current_dir = os.path.dirname(__file__)
        assets_dir = os.path.join(current_dir, "..", "assets")
        assets_dir = os.path.normpath(assets_dir)
        self.default_themes = {
            "Default": {
                "background": os.path.join(assets_dir, "default_bg.jpg"),
                "audio": [os.path.join(assets_dir, "test_audio.mp3")],
                "extra_widget": False
            },
            "Ocean": {
                "background": os.path.join(assets_dir, "ocean_bg.jpg"),
                "audio": [os.path.join(assets_dir, "test_audio.mp3")],
                "extra_widget": True,
                "extra_button_text": "Help"
            }
        }
        self.custom_themes_file = custom_themes_file
        self.custom_themes = self.load_custom_themes()
        self.themes = {**self.default_themes, **self.custom_themes}

    def load_custom_themes(self):
        if os.path.exists(self.custom_themes_file):
            with open(self.custom_themes_file, "r") as file:
                return json.load(file)
        return {}

    def save_custom_themes(self):
        with open(self.custom_themes_file, "w") as file:
            json.dump(self.custom_themes, file)

    def get_all_theme_names(self):
        return list(self.themes.keys()) + ["Add Custom Theme"]

    def get_theme_config(self, theme_name):
        return self.themes.get(theme_name)

    def create_custom_theme(self):
        bg_path = filedialog.askopenfilename(
            title="Select Background Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")]
        )
        if not bg_path:
            return

        theme_name = simpledialog.askstring("Theme Name", "Enter a name for your custom theme:")
        if not theme_name:
            return

        self.custom_themes[theme_name] = {
            "background": bg_path,
            "extra_widget": False
        }
        self.save_custom_themes()
        self.themes = {**self.default_themes, **self.custom_themes}

        messagebox.showinfo("Success", f"Custom theme '{theme_name}' created successfully!")
        return theme_name