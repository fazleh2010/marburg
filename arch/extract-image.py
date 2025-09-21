import fitz  # PyMuPDF
import os
from PIL import Image
from io import BytesIO

# Input PDF and output folder
dir = "/documents/"
pdf_name = "book_Bruggen_Israels_Machtelt_Piero_del"
pdf_path = dir + f"corpus_texts/{pdf_name}.pdf"
output_folder = dir + "extracted_images"
os.makedirs(output_folder, exist_ok=True)

# Open the PDF
doc = fitz.open(pdf_path)
images = []  # list to store PIL images
count = 0

# Loop through pages and extract images
for page_number in range(len(doc)):
    page = doc[page_number]
    image_list = page.get_images(full=True)

    if not image_list:
        continue  # skip pages with no images

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

        # Load into PIL for optional in-memory processing
        pil_image = Image.open(BytesIO(image_bytes))

        images.append({
            "page": page_number + 1,
            "index": img_index,
            "filename": filename,
            "image": pil_image
        })

        count += 1

print(f"✅ Extracted and loaded {count} images into memory.")
