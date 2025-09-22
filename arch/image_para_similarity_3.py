import os
import torch
import csv
from PIL import Image
import clip
import json
import nltk
from nltk.corpus import stopwords
import re

# Download stopwords (only first time)
nltk.download("stopwords")
STOPWORDS = set(stopwords.words("english"))

def clean_text(text):
    """
    Remove stopwords, punctuation, digits, and short words from a string.
    """
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)   # keep only letters & spaces
    tokens = text.split()
    filtered = [w for w in tokens if w not in STOPWORDS and len(w) > 2]
    return " ".join(filtered)

def load_clip_model(device="cuda"):
    """Load CLIP model + preprocess function"""
    model, preprocess = clip.load("ViT-B/32", device=device)
    return model, preprocess

def get_image_files(image_directory, valid_extensions):
    """Get valid image file paths"""
    image_files = []
    for filename in os.listdir(image_directory):
        if filename.lower().endswith(valid_extensions):
            filepath = os.path.join(image_directory, filename)
            try:
                with Image.open(filepath) as _:
                    image_files.append(filepath)
            except Exception as e:
                print(f"⚠️ Failed to open {filename}: {e}")
    return image_files

def tokenize_with_truncate(texts, device):
    """Tokenize texts safely (truncate if >77 tokens)."""
    return clip.tokenize(texts, truncate=True).to(device)

def process_images_and_paragraphs(image_files, paragraphs, model, preprocess, device, output_dir):
    """Compute image ↔ paragraph similarities"""

    # Unpack (page, para_index, text)
    texts = [p[2] for p in paragraphs]
    tokenized_texts = tokenize_with_truncate(texts, device)

    with torch.no_grad():
        text_features = model.encode_text(tokenized_texts)
        text_features /= text_features.norm(dim=-1, keepdim=True)

    for fileName in image_files:
        print(f"\n📷 Processing Image: {fileName}")
        image = preprocess(Image.open(fileName)).unsqueeze(0).to(device)

        with torch.no_grad():
            image_features = model.encode_image(image)
            image_features /= image_features.norm(dim=-1, keepdim=True)

            sims = (image_features @ text_features.T).squeeze(0).cpu().numpy()

        # Attach metadata back
        ranked = sorted(
            [(para[0], para[1], para[2], sims[i]) for i, para in enumerate(paragraphs)],
            key=lambda x: x[3],
            reverse=True
        )

        # Print top-5
        for page, para_index, text, score in ranked[:5]:
            print(f"→ {score:.4f} | Page {page}, Paragraph {para_index}: {text[:80]}...")

        # Save to CSV
        outputfile = os.path.join(output_dir, os.path.basename(fileName) + ".csv")
        with open(outputfile, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Page", "Paragraph", "Text", "Similarity"])
            writer.writerows(ranked)

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = load_clip_model(device)

    dir = "/home/melahi/code/documents/"
    image_dir = os.path.join(dir, "extracted_images_test")
    output_dir = os.path.join(dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    image_files = get_image_files(image_dir, valid_extensions)

    prefix = "book_Bruggen_Israels_Machtelt_Piero_del"
    json_path = os.path.join(image_dir, f"{prefix}.json")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    paragraphs = []
    for page in data:
        page_num = page.get("page")
        for para_index, para in enumerate(page.get("paragraphs", []), start=1):
            cleaned = clean_text(para)
            if cleaned.strip():
                # Store (page, paragraph_index, text)
                paragraphs.append((page_num, para_index, cleaned))

    print(f"✅ Loaded {len(paragraphs)} cleaned paragraphs")

    process_images_and_paragraphs(image_files, paragraphs, model, preprocess, device, output_dir)

if __name__ == "__main__":
    main()
