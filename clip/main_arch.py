import os
import json
import fitz  # PyMuPDF
from langdetect import detect, LangDetectException

def get_pdf_files(directory):
    """Returns a list of PDF files in the specified directory."""
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.lower().endswith('.pdf')
    ]

def detect_language(text):
    """Detects the language of a given text string."""
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"

def extract_text_and_images_with_lang(pdf_path, image_output_dir):
    """Extracts text, language, and images from a PDF file."""
    data = {}
    pdf_name = os.path.basename(pdf_path)
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_data = {}

        # Extract text and detect language
        text = page.get_text().strip()
        lang = detect_language(text)
        page_data["text"] = text
        page_data["language"] = lang

        # Extract images
        images = page.get_images(full=True)
        image_paths = []

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]

            image_filename = f"{os.path.splitext(pdf_name)[0]}_page{page_num+1}_img{img_index+1}.{ext}"
            image_path = os.path.join(image_output_dir, image_filename)

            if not os.path.exists(image_output_dir):
                os.makedirs(image_output_dir)

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            image_paths.append(image_path)

        page_data["images"] = image_paths
        data[str(page_num + 1)] = page_data

    doc.close()
    return pdf_name, data

def process_pdfs_with_text_and_images(input_dir, output_json_path, image_output_dir):
    """Processes all PDFs in a directory and saves structured JSON with text, language, and image info."""
    pdf_files = get_pdf_files(input_dir)
    result = {}

    for pdf_path in pdf_files:
        print(f"Processing: {pdf_path}")
        filename, pdf_data = extract_text_and_images_with_lang(pdf_path, image_output_dir)
        result[filename] = pdf_data

    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Done. JSON saved to: {output_json_path}")

# === Example usage ===
if __name__ == "__main__":
    input_directory = "/home/melahi/code/image-data/pdfs/"
    output_json_path = "/home/melahi/code/image-data/output/pdf_data.json"
    image_output_directory = "/home/melahi/code/image-data/extracted_images/"
    process_pdfs_with_text_and_images(input_directory, output_json_path, image_output_directory)
