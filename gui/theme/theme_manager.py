import os
import json
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk

from gui.widgets.customise_popup import CustomPopup

class ThemeManager:
    def __init__(self, custom_themes_file="custom_themes.json"):
        current_dir = os.path.dirname(__file__)
        assets_dir = os.path.join(current_dir, "..", "assets")
        assets_dir = os.path.normpath(assets_dir)

        self.default_themes = {
            "Default": {
                "color": "#000000",
                "image": os.path.join(assets_dir, "meme.jpg"),
                "audio": [os.path.join(assets_dir, "scream.mp3"), 
                        os.path.join(assets_dir, "amongus.mp3")],
                "extra_widget": False
            },
            "Capybara": {
                "color": "#000000",
                "image": os.path.join(assets_dir, "capybara.jpg"),
                "audio": [os.path.join(assets_dir, "capybara.mp3")],
                "extra_widget": False,
                # "extra_button_text": "Help"
            },
            "Parent": {
                "color": "#000000",
                "image": os.path.join(assets_dir, "steven-he-cropped.jpg"),
                "audio": [os.path.join(assets_dir, "failure.mp3"), 
                        os.path.join(assets_dir, "emotional-damage.mp3"), 
                        os.path.join(assets_dir, "do-ur-hmwk.mp3")],
                "extra_widget": False
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

    def save_custom_theme(self, theme_name, theme_data):
        if not theme_name:
            raise ValueError("Theme name cannot be empty.")
        self.custom_themes[theme_name] = theme_data
        self.save_custom_themes()  
        self.themes[theme_name] = theme_data  # Comes from popup

    def save_custom_themes(self):
        with open(self.custom_themes_file, "w") as file:
            json.dump(self.custom_themes, file)

    def get_all_theme_names(self):
        return list(self.themes.keys()) + ["Add Custom Theme"]

    def get_theme_config(self, theme_name):
        return self.themes.get(theme_name)

    def create_custom_theme(self, parent):
        popup = CustomPopup(parent, self.themes)
        parent.wait_window(popup)  
