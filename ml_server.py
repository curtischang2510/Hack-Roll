from flask import Flask, request, jsonify
from PIL import Image
import torch
from transformers import AutoProcessor, AutoModelForVision2Seq
import io

# Initialize Flask app
app = Flask(__name__)

# Load model and processor
device = "cuda" if torch.cuda.is_available() else "cpu"
processor = AutoProcessor.from_pretrained("HuggingFaceTB/SmolVLM-Instruct")
model = AutoModelForVision2Seq.from_pretrained(
    "HuggingFaceTB/SmolVLM-Instruct",
    torch_dtype=torch.bfloat16
).to(device)

def process_image(image_data):
    """Process the image with the Vision-Language Model."""
    try:
        img = Image.open(io.BytesIO(image_data))
        # Prepare the conversation
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
        prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
        inputs = processor(text=prompt, images=[img], return_tensors="pt").to(device)

        # Generate the response
        generated_ids = model.generate(**inputs, max_new_tokens=50)
        generated_texts = processor.batch_decode(
            generated_ids,
            skip_special_tokens=True,
        )
        return generated_texts[0]  # Return the generated response
    except Exception as e:
        print(f"Error processing image: {e}")
        return "Error processing the image."

@app.route('/process-image', methods=['POST'])
def process_image_endpoint():
    """Endpoint to process an image."""
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']
    image_data = file.read()

    # Process the image and get the response
    response = process_image(image_data)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)