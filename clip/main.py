import torch
import clip
import os
from PIL import Image



device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)


# Path to your image directory
image_dir = "/home/melahi/code/CLIP/images/"

# Supported image extensions
valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')

image_files = []
texts=["a diagram", "a dog", "a cat"]

# Loop through files in the directory
for filename in os.listdir(image_dir):
    if filename.lower().endswith(valid_extensions):
        filepath = os.path.join(image_dir, filename)
        try:
            with Image.open(filepath) as img:
                print(f"{filename}: size={img.size}, mode={img.mode}")
                image_files.append(image_dir+filename)
        except Exception as e:
            print(f"Failed to open {filename}: {e}")

for fileName in image_files:
    print(fileName)
    image = preprocess(Image.open(fileName)).unsqueeze(0).to(device)
    text = clip.tokenize(texts).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)
        logits_per_image, logits_per_text = model(image, text)
        probs = logits_per_image.softmax(dim=-1).cpu().numpy()

print("texts:", texts)
for probList in probs:
    for prob in probList:
        print(prob)

# print("Label probs:", probs)  # prints: [[0.9927937  0.00421068 0.00299572]]