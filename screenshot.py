from datetime import datetime
import torch
import time
import pyautogui
import os
from PIL import Image
from transformers import AutoProcessor, AutoModelForVision2Seq

class VLM:
    def __init__(self):
        # Directory to save screenshots
        self.screenshot_dir = "assets/screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Load model and processor once
        print("Loading model and processor...")
        self.processor = AutoProcessor.from_pretrained("HuggingFaceTB/SmolVLM-Instruct")
        self.model = AutoModelForVision2Seq.from_pretrained(
            "HuggingFaceTB/SmolVLM-Instruct",
            torch_dtype=torch.bfloat16
        ).to(self.device)
        print("Model and processor loaded.")

    def check_laptop_screen(self):
        """Takes a screenshot and sends it to the model."""
        try:
            print("Taking a screenshot...")
            # Get current timestamp for file name
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_path = os.path.join(self.screenshot_dir, f"screenshot_{timestamp}.png")

            # Take the screenshot
            screenshot = pyautogui.screenshot()
            screenshot.save(file_path)
            print(f"Screenshot saved: {file_path}")
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return

        # Send the screenshot to VLM
        answer = self.query_vlm(file_path)
        print(f"Model response: {answer}")
        return "yes" in answer.lower()

    def query_vlm(self, screenshot_path):
        """Query the Vision-Language Model with the screenshot."""
        try:
            # Prepare a single conversation
            conversation = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image"},
                        {"type": "text", "text": "Is this screen related to work, study, research, programming, or STEM? Reply 'yes'. If related to leisure reply 'no'."}
                    ],
                }
            ]

            # Prepare inputs
            img = Image.open(screenshot_path)
            prompt = self.processor.apply_chat_template(conversation, add_generation_prompt=True)
            inputs = self.processor(text=prompt, images=[img], return_tensors="pt")
            inputs = inputs.to(self.device)

            # Generate the response
            generated_ids = self.model.generate(**inputs, max_new_tokens=3)
            generated_texts = self.processor.batch_decode(
                generated_ids,
                skip_special_tokens=True,
            )

            if "Assistant:" in generated_texts[0]:
                assistant_response = generated_texts[0].split("Assistant:")[1].strip()
                return assistant_response
            return "No valid response from the model."
        except Exception as e:
            print(f"Error in query_vlm: {e}")
            return "Error occurred during processing."