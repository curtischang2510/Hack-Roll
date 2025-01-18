import tkinter as tk
import time

class TimerWidget(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.sv = tk.StringVar()
        self.start_time = None
        self.is_running = False

        self.make_widgets()
        self.bind_events()

    def make_widgets(self):
        """Create widgets for the timer."""
        self.canvas = tk.Canvas(self, width=25, height=25)
        self.canvas.pack(side=tk.LEFT, padx=10)
        self.red_circle = self.canvas.create_oval(5, 5, 20, 20, fill="red", outline="brown4")

        self.label = tk.Label(self, textvariable=self.sv, font="Arial 15")
        self.label.pack(side=tk.LEFT)

    def bind_events(self):
        """Bind events to start/stop timer."""
        self.canvas.tag_bind(self.red_circle, "<Button-1>", self.startstop)

    def timer(self):
        """Update the timer display."""
        elapsed = time.time() - self.start_time
        self.sv.set(self.format_time(elapsed))
        self.after_loop = self.after(50, self.timer)

    def start(self):
        if not self.is_running:
            self.start_time = time.time()
            self.timer()
            self.is_running = True
            print("Timer started")

    def stop(self):
        if self.is_running:
            self.after_cancel(self.after_loop)
            self.is_running = False
            print("Timer stopped")

    def startstop(self, event=None):
        if self.is_running:
            self.stop()
        else:
            self.start()

    @staticmethod
    def format_time(elap):
        """Format elapsed time into hh:mm:ss.t"""
        hours = int(elap / 3600)
        minutes = int(elap / 60 - hours * 60)
        seconds = int(elap - hours * 3600 - minutes * 60)
        tenths = int((elap - hours * 3600 - minutes * 60 - seconds) * 10)
        return '%02d:%02d:%02d:%1d' % (hours, minutes, seconds, tenths)
