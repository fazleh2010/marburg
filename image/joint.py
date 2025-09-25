import os
import json
import re
import torch
from PIL import Image
from langdetect import detect
from transformers import CLIPProcessor, CLIPModel

# ----------------- Utility Functions -----------------

def load_clip_model(device):
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    return model, processor

def clean_text(text):
    # Additional cleaning rules if needed
    return text.strip().lower()

def split_text(text, max_tokens=77):
    """
    Split text into chunks of <= max_tokens words (CLIP limit)
    """
    words = text.split()
    chunks = [words[i:i+max_tokens] for i in range(0, len(words), max_tokens)]
    return [" ".join(chunk) for chunk in chunks]

def process_images_and_texts(image_files, texts, model, processor, device,
                             output_dir, page_num, para_index, original_para):
    """
    Match a paragraph with a list of images using CLIP.
    Properly handles long text using processor truncation.
    """
    best_file = None
    best_score = -1
    scores = []

    for img_path in image_files:
        image = Image.open(img_path).convert("RGB")

        # Preprocess with truncation
        inputs = processor(
            text=texts,
            images=image,
            return_tensors="pt",
            padding=True,
            truncation=True,  # <-- ensures sequence <= 77 tokens
        ).to(device)

        with torch.no_grad():
            outputs = model(**inputs)
            image_embeds = outputs.image_embeds
            text_embeds = outputs.text_embeds

        # Normalize embeddings
        image_embeds = image_embeds / image_embeds.norm(p=2, dim=-1, keepdim=True)
        text_embeds = text_embeds / text_embeds.norm(p=2, dim=-1, keepdim=True)

        # Cosine similarity
        similarity = torch.matmul(text_embeds, image_embeds.T)  # [num_texts, 1]
        score = similarity.max().item()  # max similarity if multiple texts

        scores.append({
            "image": os.path.basename(img_path),
            "similarity": score
        })

        if score > best_score:
            best_score = score
            best_file = os.path.basename(img_path)

    return best_file, scores

# ----------------- Main Workflow -----------------

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, processor = load_clip_model(device)

    base_dir = "/home/melahi/code/documents/"
    image_dir = os.path.join(base_dir, "extracted_images_test")
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')

    # Step 1: find all JSON files and sort by size (largest first)
    json_files = [f for f in os.listdir(image_dir) if f.endswith(".json")]


    print(f"Found {len(json_files)} JSON files, sorted by size (largest first):")
    for jf in json_files:
        size_kb = os.path.getsize(os.path.join(image_dir, jf)) / 1024
        print(f"  {jf} - {size_kb:.1f} KB")

    for json_file in json_files:
        prefix = os.path.splitext(json_file)[0]
        json_path = os.path.join(image_dir, json_file)


        # Step 2: check language
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        all_text = " ".join(
            para for page in data for para in page.get("paragraphs", [])
        )

        if not all_text.strip():
            print(f"⚠️ {prefix}: Empty JSON, skipping...")
            continue

        try:
            lang = detect(all_text)
        except:
            print(f"⚠️ {prefix}: Could not detect language, skipping...")
            continue

        if lang not in ["en"]:
            print(f"⚠️ {prefix}: Detected language '{lang}', skipping...")
            continue

        print(f"\n🔎 Processing prefix: {prefix} | Language: {lang}")

        # Step 3: get matching images
        image_files = [
            os.path.join(image_dir, f) for f in os.listdir(image_dir)
            if f.startswith(prefix) and f.lower().endswith(valid_extensions)
        ]

        if not image_files:
            print(f"⚠️ {prefix}: No images found, skipping...")
            continue

        final_results = []

        for page in data:
            page_num = page.get("page")
            paragraphs = page.get("paragraphs", [])

            for para_index, para in enumerate(paragraphs, start=1):
                original_para = para
                texts = split_text(para)  # Split into <=77 token chunks

                print(f"\n=== {prefix} | Page {page_num}, Paragraph {para_index} ==="+"\n"+para)

                fileName, probabilityValue = process_images_and_texts(
                    image_files, texts, model, processor, device,
                    output_dir, page_num, para_index, original_para
                )

                final_results.append({
                    "image": fileName,
                    "page": page_num,
                    "paragraph_number": para_index,
                    "original_text": original_para,
                    "results": probabilityValue
                })

        # Step 4: write results
        output_json = os.path.join(output_dir, f"{prefix}_results.json")
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(final_results, f, indent=2, ensure_ascii=False)
        print(f"✅ Results saved: {output_json}")


if __name__ == "__main__":
    main()
