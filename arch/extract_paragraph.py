import fitz  # PyMuPDF
import json
import os


dir= "/documents/"
pdf_path = dir+"corpus_texts/book_Bruggen_Israels_Machtelt_Piero_del.pdf"
output_json = dir+"extracted_images"+"/book_Bruggen_Israels_Machtelt_Piero_del.json"

doc = fitz.open(pdf_path)
pages_data = []

for page_num in range(len(doc)):
    page = doc[page_num]

    # Extract blocks: (x0, y0, x1, y1, "text", block_no, block_type)
    blocks = page.get_text("blocks")

    # Filter out only text blocks (block_type == 0)
    text_blocks = [b for b in blocks if b[6] == 0]

    # Sort first by column (x0), then by y (top-down)
    text_blocks.sort(key=lambda b: (round(b[0] / 50), b[1]))

    # Store each block (paragraph) separately
    paragraphs = []
    for b in text_blocks:
        text = b[4].strip()
        if text:
            paragraphs.append(text)

    pages_data.append({
        "page": page_num + 1,
        "paragraphs": paragraphs
    })

# Save JSON
os.makedirs(os.path.dirname(output_json), exist_ok=True)
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(pages_data, f, ensure_ascii=False, indent=2)

print(f"✅ Extracted paragraphs from {len(doc)} pages and saved to {output_json}")