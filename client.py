import socket 
import pyautogui
import os
from datetime import datetime

class Screenchecker: 
    def __init__(self):
        self.screenshot_dir = "assets/screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def check_screen(self):
        # Get current timestamp for file name
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = os.path.join(self.screenshot_dir, f"screenshot_{timestamp}.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(file_path)
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('SERVER_IP', 5000))

        with open(file_path, 'rb') as f: 
            image_data = f.read()
            client.sendall(image_data)
        
        response = client.recv(1024)
        print("Response from server:", response.decode())
        client.close()
