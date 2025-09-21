import os
from PIL import Image
import json

# --- Settings ---
dir="/home/melahi/code/documents/"
folder = dir+"/extracted_images"
prefix = "book_Bruggen_Israels_Machtelt_Piero_del"
json_path = os.path.join(folder, f"{prefix}.json")

# --- Load all images ---
images = []
for filename in os.listdir(folder):
    if filename.startswith(prefix) and filename.lower().endswith((".png", ".jpg", ".jpeg")):
        filepath = os.path.join(folder, filename)
        try:
            img = Image.open(filepath)
            images.append({
                "filename": filename,
                "image": img
            })
        except Exception as e:
            print(f"⚠️ Could not open {filename}: {e}")

print(f"✅ Loaded {len(images)} images starting with '{prefix}' from {folder}\n")

# --- Load paragraphs from JSON ---
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- Iterate over images, pages, and paragraphs ---
for img_info in images:
    print(f"=== Image: {img_info['filename']} ===\n")

    for page in data:
        page_num = page.get("page")
        paragraphs = page.get("paragraphs", [])
        for para_index, para in enumerate(paragraphs, start=1):
            # Print full paragraph
            print(f"Page {page_num}, Paragraph {para_index}: {para}\n")

    print("\n")  # separate images
