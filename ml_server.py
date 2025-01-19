from multiprocessing import process
import socket
from urllib import response
from PIL import Image 
import torch
from transformers import AutoProcessor, AutoModelForVision2Seq
import io

device = "cuda" if torch.cuda.is_available() else "cpu"
processor = AutoProcessor.from_pretrained("HuggingFaceTB/SmolVLM-Instruct")
model = AutoModelForVision2Seq.from_pretrained(
    "HuggingFaceTB/SmolVLM-Instruct",
    torch_dtype=torch.bfloat16
).to(device)

def process_image(image_data):
    img = Image.open(io.BytesIO(image_data))
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
    prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
    inputs = processor(text=prompt, images=[img], return_tensors="pt")
    inputs = inputs.to(device)

    # Generate the response
    generated_ids = model.generate(**inputs, max_new_tokens=50)
    generated_texts = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True,
    )
    return generated_texts[0]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind('0.0.0.0', 5000)
server_socket.listen()
print("Server is listening...")

while True: 
    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")
    data = conn.recv()
    response = process_image(data)
    conn.sendall(response.encode(10 * 1024 * 1024))
    conn.close()