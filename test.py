from datetime import datetime
import torch
import time
import pyautogui
import os
from PIL import Image
from transformers import AutoProcessor, AutoModelForVision2Seq

# Directory to save screenshots
screenshot_dir = "assets/screenshots"
os.makedirs(screenshot_dir, exist_ok=True)
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load model and processor once
processor = AutoProcessor.from_pretrained("HuggingFaceTB/SmolVLM-Instruct")
model = AutoModelForVision2Seq.from_pretrained(
    "HuggingFaceTB/SmolVLM-Instruct",
    torch_dtype=torch.bfloat16
).to(device)

def check_laptop_screen():
    """Takes a screenshot and saves it to a file."""
    try:
        # Get current timestamp for file name
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")

        # Take the screenshot
        print("before screenshot")
        screenshot = pyautogui.screenshot()
        screenshot.save(file_path)
        print(f"Screenshot saved: {file_path}")

        # Send the screenshot to VLM
        answer = query_vlm(file_path)
        print(f"Model Answer: {answer}")
    except Exception as e:
        print(f"Error in check_laptop_screen: {e}")

def query_vlm(screenshot_path):
    try:
        # Prepare a single conversation
        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "image"},
                    {"type": "text", "text": "Is this screen related to work, study, or research? Reply 'yes' for work/study and 'no' for leisure/play."}
                ],
            }
        ]

        # Prepare inputs
        prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
        inputs = processor(text=prompt, images=[Image.open(screenshot_path)], return_tensors="pt")
        inputs = inputs.to(device)

        # Generate the response
        generated_ids = model.generate(**inputs, max_new_tokens=3)
        generated_texts = processor.batch_decode(
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

def main():
    # try:
    #     iteration = 0
    #     max_iterations = 10  # Limit to 10 iterations for safety
    #     while iteration < max_iterations:
    #         check_laptop_screen()
    #         time.sleep(10)  # Wait for 10 seconds
    #         iteration += 1
    # except KeyboardInterrupt:
    #     print("Stopped by user.")
    # except Exception as e:
    #     print(f"Error in main loop: {e}")
    print("reached")
    check_laptop_screen()

if __name__ == "__main__":
    main()
