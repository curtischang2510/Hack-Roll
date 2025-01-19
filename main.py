import threading
from gui.main_window import MainWindow
from open_cv import OpenCV

def openCV_callback(user_looking, frame):
    """Callback to pass frames to the MainWindow instance."""
    if frame is not None:
        app.set_latest_frame(frame)  # Update the frame in MainWindow

if __name__ == "__main__":
    print("Starting application...")
    opencv = OpenCV(callback=openCV_callback)
    app = MainWindow(opencv)
    print("Starting Tkinter main loop...")

    thread = threading.Thread(target=opencv.run, daemon=True)
    thread.start()
    print("OpenCV thread started.")

    try:
        app.mainloop()
        print("Tkinter main loop running.")
    except Exception as e:
        print(f"Error in Tkinter main loop: {e}")
    finally:
        opencv.stop()
        print("Application exited.")