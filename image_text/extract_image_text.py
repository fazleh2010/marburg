import fitz  # PyMuPDF
import os
from PIL import Image
from io import BytesIO
import json

# Input PDF and output folder
dir = "/home/melahi/code/marburg/documents/"
pdf_name = "book_Bruggen_Israels_Machtelt_Piero_del"
pdf_path = dir + f"corpus_texts/{pdf_name}.pdf"

output_folder = dir + "extracted_images"
os.makedirs(output_folder, exist_ok=True)

output_json = os.path.join(output_folder, f"{pdf_name}.json")

# Open the PDF
doc = fitz.open(pdf_path)

# Initialize storage
images = []      # list of PIL images and metadata
pages_data = []  # list of text paragraphs per page
image_count = 0

# Loop through pages
for page_number in range(len(doc)):
    page = doc[page_number]

    ### --- Extract images ---
    image_list = page.get_images(full=True)
    if image_list:
        for img_index, img in enumerate(image_list, start=1):
            xref = img[0]  # XREF of the image
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]

            # Filename with book prefix
            filename = f"{pdf_name}_page{page_number+1}_img{img_index}.{ext}"
            filepath = os.path.join(output_folder, filename)

            # Save image to disk
            with open(filepath, "wb") as f:
                f.write(image_bytes)

            # Load into PIL for in-memory processing
            pil_image = Image.open(BytesIO(image_bytes))

            images.append({
                "page": page_number + 1,
                "index": img_index,
                "filename": filename,
                "image": pil_image
            })

            image_count += 1

    ### --- Extract text ---
    blocks = page.get_text("blocks")
    text_blocks = [b for b in blocks if b[6] == 0]  # only text
    text_blocks.sort(key=lambda b: (round(b[0] / 50), b[1]))  # column-wise reading

    paragraphs = []
    for b in text_blocks:
        text = b[4].strip()
        if text:
            paragraphs.append(text)

    pages_data.append({
        "page": page_number + 1,
        "paragraphs": paragraphs
    })

# Save paragraphs to JSON
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(pages_data, f, ensure_ascii=False, indent=2)

print(f"✅ Extracted and saved {image_count} images to {output_folder}")
print(f"✅ Extracted paragraphs from {len(doc)} pages and saved to {output_json}")
