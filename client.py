import requests
import pyautogui
from datetime import datetime
import os
import time

SERVER_URL = "http://172.20.10.14:5000/process-image"  # Update with your server's IP and port

class Screenchecker:
    def __init__(self):
        # Create a directory for screenshots
        self.screenshot_dir = "assets/screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def take_screenshot(self):
        # Generate a timestamp for the filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = os.path.join(self.screenshot_dir, f"screenshot_{timestamp}.png")

        # Capture and save the screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(file_path)
        print(f"[DEBUG] Screenshot saved: {file_path}")
        return file_path

    def send_screenshot(self, file_path):
        # Open the screenshot file and send it to the server
        with open(file_path, 'rb') as f:
            files = {'image': (os.path.basename(file_path), f, 'image/png')}
            try:
                response = requests.post(SERVER_URL, files=files)
                if response.status_code == 200:
                    print(f"[DEBUG] Server response: {response.json()}")
                else:
                    print(f"[ERROR] Server returned status {response.status_code}: {response.text}")
            except Exception as e:
                print(f"[ERROR] Failed to send image: {e}")

    def run(self):
        # Continuously take screenshots and send them to the server every 10 seconds
        try:
            while True:
                screenshot_path = self.take_screenshot()
                self.send_screenshot(screenshot_path)
                time.sleep(5)  # Wait for 10 seconds between screenshots
        except KeyboardInterrupt:
            print("[INFO] Stopping the screen checker.")

if __name__ == "__main__":
    checker = Screenchecker()
    checker.run()