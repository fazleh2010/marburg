import os
import json
import fitz  # PyMuPDF

def get_pdf_files(directory):
    """Returns all PDF file paths in a directory."""
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.lower().endswith('.pdf')
    ]

def extract_text_and_images(pdf_path, output_image_dir):
    """Extracts text and images from a PDF file."""
    data = {}
    pdf_name = os.path.basename(pdf_path)
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_data = {}

        # Extract text
        page_text = page.get_text()
        page_data['text'] = page_text.strip()

        # Extract images
        image_info_list = []
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]

            # Construct image filename
            image_filename = f"{os.path.splitext(pdf_name)[0]}_page{page_num+1}_img{img_index+1}.{ext}"
            image_path = os.path.join(output_image_dir, image_filename)

            # Save image
            if not os.path.exists(output_image_dir):
                os.makedirs(output_image_dir)
            with open(image_path, "wb") as f:
                f.write(image_bytes)

            image_info_list.append(image_path)

        page_data['images'] = image_info_list
        data[str(page_num + 1)] = page_data

    doc.close()
    return pdf_name, data

def process_all_pdfs(input_dir, output_json, image_output_dir):
    """Processes all PDFs and saves results to a JSON file."""
    pdf_files = get_pdf_files(input_dir)
    all_data = {}

    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file}")
        filename, pdf_data = extract_text_and_images(pdf_file, image_output_dir)
        all_data[filename] = pdf_data

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Finished. Data saved to: {output_json}")

# === Example usage ===
if __name__ == "__main__":
    input_directory = "/home/melahi/code/image-data/test/"
    output_json_path = "/home/melahi/code/image-data/output/pdf_data.json"
    image_output_directory="/home/melahi/code/image-data/extracted_images/"
    process_all_pdfs(input_directory, output_json_path, image_output_directory)
