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
        theme_name = self.name_var.get().strip()  # Remove leading/trailing spaces
        if theme_name:
            self.theme_data["name"] = theme_name
            self.themes[theme_name] = self.theme_data
            self.parent.update_theme_dropdown()
            print(f"Theme '{theme_name}' saved!") 

            # Temporarily update button text
            original_text = self.save_button["text"]
            self.save_button.config(text="Theme Saved!", state="disabled")
            self.after(2000, lambda: self.save_button.config(text=original_text, state="normal"))

            self.destroy()
        else:
            # Visual feedback for missing theme name
            self.name_entry.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)
            print("Theme name cannot be empty!") 
            # Restore border to default after 2 seconds
            self.after(2000, lambda: self.name_entry.config(highlightthickness=0))

# class MainApp(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Main App")
#         self.geometry("400x300")

#         self.themes = {
#             "Default": {
#                 "name": "Default",
#                 "color": "#ffffff",
#                 "image": None,
#                 "audio": ["default1.mp3", "default2.mp3", "default3.mp3", "default4.mp3"],
#             }
#         }

#         self.current_theme = "Default"
#         self.init_ui()

#     def init_ui(self):
#         self.theme_var = tk.StringVar(value=self.current_theme)

#         label = tk.Label(self, text="Select Theme:")
#         label.pack(pady=5)

#         self.dropdown = ttk.Combobox(self, textvariable=self.theme_var, values=list(self.themes.keys()), state="readonly")
#         self.dropdown.pack(pady=5)
#         self.dropdown.bind("<<ComboboxSelected>>", self.apply_theme)

#         button = tk.Button(self, text="Customize Theme", command=self.open_popup)
#         button.pack(pady=10)

#         self.test_button = tk.Button(self, text="Simulate Distraction", command=self.simulate_distraction)
#         self.test_button.pack(pady=10)

#     def open_popup(self):
#         CustomPopup(self, self.themes)

#     def apply_theme(self, event=None):
#         selected_theme = self.theme_var.get()
#         theme_data = self.themes.get(selected_theme, {})
#         self.current_theme = selected_theme

#         # Update background color and image
#         self.configure(bg=theme_data.get("color", "#ffffff"))
#         if theme_data.get("image"):
#             self.bg_image = tk.PhotoImage(file=theme_data["image"])
#             bg_label = tk.Label(self, image=self.bg_image)
#             bg_label.place(relwidth=1, relheight=1)

#         print(f"Applied theme: {selected_theme}")  # Debug

#     def update_theme_dropdown(self):
#         self.dropdown["values"] = list(self.themes.keys())

#     def simulate_distraction(self):
#         """Simulate a distraction and play the corresponding audio."""
#         theme_data = self.themes.get(self.current_theme, {})
#         if theme_data["audio"]:
#             audio_file = theme_data["audio"][0]  # Use audio for first scenario as example
#             if audio_file:
#                 threading.Thread(target=playsound, args=(audio_file,), daemon=True).start()
#                 print(f"Playing audio: {audio_file}")  # Debug
#             else:
#                 print("No audio file set for this theme!")  # Debug


# if __name__ == "__main__":
#     app = MainApp()
#     app.mainloop()
