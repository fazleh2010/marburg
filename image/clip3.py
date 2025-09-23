import os
import torch
from PIL import Image
import clip
import json
import nltk
from nltk.corpus import stopwords
import re

# Download stopwords (only the first time)
nltk.download("stopwords")
STOPWORDS = set(stopwords.words("english"))


def clean_text(text):
    """
    Remove stopwords, punctuation, and extra whitespace from a string.
    """
    # Lowercase
    text = text.lower()
    # Remove all non-alphanumeric characters (punctuation, symbols)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    # Split into words and remove stopwords
    tokens = text.split()
    filtered = [word for word in tokens if word not in STOPWORDS]
    # Join back into string
    return " ".join(filtered)


def load_clip_model(device="cuda"):
    """Load the CLIP model and preprocessing function."""
    model, preprocess = clip.load("ViT-B/32", device=device)
    return model, preprocess


def get_image_files(image_directory, valid_extensions):
    """Get all valid image file paths from the given directory."""
    image_files = []
    for filename in os.listdir(image_directory):
        if filename.lower().endswith(valid_extensions):
            filepath = os.path.join(image_directory, filename)
            try:
                with Image.open(filepath) as img:
                    image_files.append(filepath)
            except Exception as e:
                print(f"⚠️ Failed to open {filename}: {e}")
    return image_files


def tokenize_with_truncate(texts, device):
    """
    Tokenize texts safely by truncating them if they exceed CLIP's max length (77 tokens).
    """
    tokenized = []
    valid_texts = []
    for t in texts:
        cleaned = clean_text(t)
        tokens = clip.tokenize([cleaned], truncate=True)  # auto-truncate
        tokenized.append(tokens[0])
        valid_texts.append(cleaned)
    return torch.stack(tokenized).to(device), valid_texts


def process_images_and_texts(image_files, texts, model, preprocess, device):
    """Process the images and texts, compute image-text similarities."""
    results = []

    for fileName in image_files:
        image = preprocess(Image.open(fileName)).unsqueeze(0).to(device)

        # Tokenize after cleaning
        text, valid_texts = tokenize_with_truncate(texts, device)

        with torch.no_grad():
            logits_per_image, logits_per_text = model(image, text)
            probs = logits_per_image.softmax(dim=-1).cpu().numpy()

            for probList in probs:
                data = []
                for idx, prob in enumerate(probList):
                    data.append({"text": valid_texts[idx], "probability": float(prob)})

                # Sort descending
                data.sort(key=lambda x: x["probability"], reverse=True)
                top_results = data[:10]

                results.append({
                    "image": os.path.basename(fileName),
                    "matches": top_results
                })

    return results


def text_to_list(textsString):
    texts = textsString.split()
    unique_words = list(set(texts))
    return unique_words


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

    final_results = []

    for page in data:
        page_num = page.get("page")
        paragraphs = page.get("paragraphs", [])

        for para_index, para in enumerate(paragraphs, start=1):
            original_text = para  # keep original before cleaning

            # Clean version
            para_clean = re.sub(r'\s+', ' ', para)
            para_clean = re.sub(r'[^a-zA-Z0-9\s]', '', para_clean)
            para_clean = re.sub(r'\d+', '', para_clean)
            para_clean = " ".join([word for word in para_clean.split() if len(word) > 2])
            para_clean = clean_text(para_clean)
            texts = text_to_list(para_clean)

            # Run CLIP similarity
            results = process_images_and_texts(image_files, texts, model, preprocess, device)

            final_results.append({
                "page": page_num,
                "paragraph_number": para_index,
                "original_text": original_text,
                "results": results
            })

    # Save to JSON
    output_json = os.path.join(output_dir, f"{prefix}_results.json")
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(final_results, f, indent=2, ensure_ascii=False)

    print(f"✅ Results written to {output_json}")


if __name__ == "__main__":
    main()
