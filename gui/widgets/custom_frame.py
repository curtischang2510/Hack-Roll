from PIL import Image, ImageTk
import tkinter as tk


class CustomFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super(CustomFrame, self).__init__(parent, borderwidth=0, highlightthickness=0, **kwargs)
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.original_img = None
        self.img = None
        self.widget_references = []
        self.bind("<Configure>", self.resize_image)

    def set_background(self, image_path):
        """Set the background image."""
        self.original_img = Image.open(image_path)
        self.resize_image()

    def resize_image(self, event=None):
        """Resize the background image dynamically."""
        if not self.original_img:
            return

        # Get the new dimensions
        width = self.winfo_width()
        height = self.winfo_height()

        if width > 0 and height > 0:
            resized_img = self.original_img.resize((width, height), Image.Resampling.LANCZOS)
            self.img = ImageTk.PhotoImage(resized_img)

            # Clear and redraw the canvas
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

            # Re-add all widgets on top
            for widget_ref in self.widget_references:
                self.canvas.create_window(widget_ref["x"], widget_ref["y"], anchor=tk.NW, window=widget_ref["widget"])

    def add(self, widget, x, y):
        """Add a widget to the canvas."""
        self.widget_references.append({"widget": widget, "x": x, "y": y})
        self.canvas.create_window(x, y, anchor=tk.NW, window=widget)