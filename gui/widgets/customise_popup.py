import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, colorchooser

class CustomPopup(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Customise Theme")

        self.name_var = tk.StringVar()  # Store the name input later

        self.custom_name()
        self.color_row()
        self.image_row()
        self.audio_tabs()

    def custom_name(self):
        frame = tk.Frame(self)
        frame.pack(fill="x", pady=10)

        label = tk.Label(frame, text="Name:")
        label.pack(side="left", padx=5)

        entry = tk.Entry(frame, textvariable=self.name_var)
        entry.pack(side="left", padx=5)

        button = tk.Button(frame, text="Submit Name", command=self.submit_name)
        button.pack(side="left", padx=5)

    def submit_name(self):
        name = self.name_var.get()
        if name:
            print(f"Entered Name: {name}")  
            self.parent.update_name(name)  # Call parent method to handle the name

    def color_row(self):
        frame = tk.Frame(self)
        frame.pack(fill="x", pady=10)

        label = tk.Label(frame, text="Background Color:")
        label.pack(side="left", padx=5)

        button = tk.Button(frame, text="Choose Color", command=self.choose_color, bd=1)
        button.pack(side="left")

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose a background color")[1]
        if color_code:
            print(f"Selected Color: {color_code}")  
            self.parent.update_background_color(color_code)

    def image_row(self):
        frame = tk.Frame(self)
        frame.pack(fill="x", pady=10)

        label = tk.Label(frame, text="Background Image:")
        label.pack(side="left", padx=5)

        button = tk.Button(frame, text="Upload Image", command=self.upload_image, bd=1)
        button.pack(side="left")

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            print(f"Selected Image: {file_path}") 
            self.parent.update_background_image(file_path)

    def audio_tabs(self):
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both", pady=10)

        for i in range(1, 5):
            tab = ttk.Frame(notebook)
            notebook.add(tab, text=f"Audio {i}")

            label = tk.Label(tab, text=f"Upload Audio for Scenario {i}")
            label.pack(pady=5)

            button = tk.Button(tab, text="Upload Audio", command=lambda tab_num=i: self.upload_audio(tab_num))
            button.pack(pady=5)

    def upload_audio(self, tab_num):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
        if file_path:
            print(f"Audio for Tab {tab_num}: {file_path}")  # Debug


# class MainApp(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Main App")
#         self.geometry("400x200")
        
#         self.name_label = tk.Label(self, text="Name: Default theme", font=("Arial", 14))
#         self.name_label.pack(pady=20)

#         button = tk.Button(self, text="Open Widget", command=self.open_popup)
#         button.pack(pady=50)

#     def open_popup(self):
#         CustomPopup(self)

#     def update_name(self, name):
#         """Update the displayed name."""
#         self.name_label.config(text=f"Name: {name}")

#     def update_background_color(self, color):
#         """Update the root window's background color."""
#         self.configure(bg=color)

#     def update_background_image(self, image_path):
#         """Update the root window's background with an image."""
#         self.bg_image = tk.PhotoImage(file=image_path)  # Store reference 
#         background_label = tk.Label(self, image=self.bg_image)
#         background_label.place(relwidth=1, relheight=1)  
#         print(f"Background image set to: {image_path}")  


# if __name__ == "__main__":
#     app = MainApp()
#     app.mainloop()
