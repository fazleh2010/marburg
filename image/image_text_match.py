import torch
import clip
from PIL import Image

# 1. Load model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# 2. Load image
image_path = "example.jpg"
image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)

# 3. Paragraph (can be long, so truncate if needed)
paragraph = """Raphael’s letter describes the importance of preserving ancient Roman ruins 
as part of cultural heritage and artistic inspiration for future generations."""

# 4. Tokenize paragraph
text = clip.tokenize([paragraph]).to(device)

# 5. Encode image + text
with torch.no_grad():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text)

# 6. Normalize (unit vectors)
image_features /= image_features.norm(dim=-1, keepdim=True)
text_features /= text_features.norm(dim=-1, keepdim=True)

# 7. Compute similarity
similarity = (image_features @ text_features.T).item()

print(f"Similarity Score: {similarity:.4f}")
