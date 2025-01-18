import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk
from playsound import playsound
import threading


class CustomPopup(tk.Toplevel):
    def __init__(self, parent, themes):
        super().__init__(parent)
        self.parent = parent
        self.themes = themes  
        self.theme_data = {"name": "", "color": None, "image": None, "audio": [None] * 4}
        self.title("Customise Theme")

        self.custom_name()
        self.color_row()
        self.image_row()
        self.audio_tabs()
        self.save_button()

    def custom_name(self):
        frame = tk.Frame(self)
        frame.pack(fill="x", pady=10)

        label = tk.Label(frame, text="Theme Name:")
        label.pack(side="left", padx=5)

        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(frame, textvariable=self.name_var)
        self.name_entry.pack(side="left")

    def color_row(self):
        frame = tk.Frame(self)
        frame.pack(fill="x", pady=10)

        label = tk.Label(frame, text="Background Color:")
        label.pack(side="left", padx=5)

        button = tk.Button(frame, text="Choose Color", command=self.choose_color)
        button.pack(side="left")

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose a background color")[1]
        if color_code:
            self.theme_data["color"] = color_code
            print(f"Selected Color: {color_code}")  # Debug

    def image_row(self):
        frame = tk.Frame(self)
        frame.pack(fill="x", pady=10)

        label = tk.Label(frame, text="Background Image:")
        label.pack(side="left", padx=5)

        button = tk.Button(frame, text="Upload Image", command=self.upload_image)
        button.pack(side="left")

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg")])
        if file_path:
            try:
                img = Image.open(file_path)  
                self.bg_image = ImageTk.PhotoImage(img)  
                print(f"Selected Image: {file_path}")
            except Exception as e:
                print(f"Error loading image: {e}")

    def audio_tabs(self):
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both", pady=10)

        for i in range(4):
            tab = ttk.Frame(notebook)
            notebook.add(tab, text=f"Audio {i+1}")

            label = tk.Label(tab, text=f"Upload Audio for Scenario {i+1}")
            label.pack(pady=5)

            button = tk.Button(tab, text="Upload Audio", command=lambda idx=i: self.upload_audio(idx))
            button.pack(pady=5)

    def upload_audio(self, idx):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3")])
        if file_path:
            self.theme_data["audio"][idx] = file_path
            print(f"Audio for Scenario {idx+1}: {file_path}")  # Debug

    def save_button(self):
        self.save_button = tk.Button(self, text="Save Theme", command=self.save_theme)  # Assign to self.save_button
        self.save_button.pack(pady=10)

    def save_theme(self):
        theme_name = self.name_var.get().strip()
        if not theme_name:
            self.name_entry.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)
            print("Theme name is empty")
            self.after(2000, lambda: self.name_entry.config(highlightthickness=0))
            return

        # Ensure valid data for color and image
        self.theme_data["name"] = theme_name
        self.theme_data["color"] = self.theme_data.get("color") or ""  # Default white color
        self.theme_data["image"] = self.theme_data.get("image") or ""  # Default: No image

        try:
            self.parent.theme_manager.save_custom_theme(theme_name, self.theme_data)
            print(f"Theme: '{theme_name}' saved!")

            original_text = self.save_button["text"]
            self.save_button.config(text="Theme Saved!", state="disabled")
            self.after(2000, lambda: self.save_button.config(text=original_text, state="normal"))
            print(f"Saving theme: {self.theme_data}")

            self.destroy()

        except Exception as e:
            print(f"Error saving theme: {e}")
