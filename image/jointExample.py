from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel

# Load pretrained CLIP model + processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Load a local image
image_path = "/home/melahi/code/documents/dog_image.jpg"
image = Image.open(image_path).convert("RGB")

# Define three paragraphs
paragraphs = [
    "A dog is playing with a ball in the grass.",
    "A cat is sleeping on a sofa.",
    "A group of people are eating dinner together."
]

# Preprocess inputs
inputs = processor(text=paragraphs, images=image, return_tensors="pt", padding=True)

# Encode image + text
with torch.no_grad():
    outputs = model(**inputs)
    image_embeds = outputs.image_embeds
    text_embeds = outputs.text_embeds

# Normalize embeddings
image_embeds = image_embeds / image_embeds.norm(p=2, dim=-1, keepdim=True)
text_embeds = text_embeds / text_embeds.norm(p=2, dim=-1, keepdim=True)

# Compute cosine similarities
similarities = torch.matmul(text_embeds, image_embeds.T)

# Find the best matching paragraph
best_idx = torch.argmax(similarities).item()
best_paragraph = paragraphs[best_idx]
best_score = similarities[best_idx].item()

# Print all similarities
for paragraph, score in zip(paragraphs, similarities):
    print(f"Paragraph: {paragraph}\nSimilarity: {score.item():.4f}\n")

print(f"✅ Best match:\nParagraph: {best_paragraph}\nScore: {best_score:.4f}")
