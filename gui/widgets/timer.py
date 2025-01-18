import tkinter as tk
import time

class Timer:
    def __init__(self):
        self.root = tk.Tk()
        self.sv = tk.StringVar()
        self.start_time = None
        self.is_running = False

        self.make_widgets()
        self.root.bind('<Return>', self.startstop)
        self.root.mainloop()

    def make_widgets(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=20)

        self.canvas = tk.Canvas(main_frame, width=25, height=25)
        self.canvas.pack(side=tk.LEFT)
        self.red_circle = self.canvas.create_oval(10, 10, 25, 25, fill="red", outline="brown4")
        
        # Binds click event 
        self.canvas.tag_bind(self.red_circle, "<Button-1>", self.startstop)

        tk.Label(main_frame, textvariable=self.sv, font="Arial 15").pack(side=tk.LEFT)

    def timer(self):
        self.sv.set(self.format_time(time.time() - self.start_time))
        self.after_loop = self.root.after(50, self.timer)

    def start(self):
        if not self.is_running:
            self.start_time = time.time()
            self.timer()
            self.is_running = True
            print("Timer started")  # debug

    def stop(self):
        if self.is_running:
            self.root.after_cancel(self.after_loop)
            self.is_running = False
            print("Timer stopped")  # debug

    def startstop(self, event=None):
        if self.is_running:
            self.stop()
        else:
            self.start()

    @staticmethod
    def format_time(elap):
        hours = int(elap / 3600)
        minutes = int(elap / 60 - hours * 60.0)
        seconds = int(elap - hours * 3600.0 - minutes * 60.0)
        hseconds = int((elap - hours * 3600.0 - minutes * 60.0 - seconds) * 10)
        return '%02d:%02d:%02d:%1d' % (hours, minutes, seconds, hseconds)


Timer()
