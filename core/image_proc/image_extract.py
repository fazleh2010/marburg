import fitz  # PyMuPDF
import os

def extract_images_from_pdf(pdf_path, output_dir):
    """
    Extracts all images from a PDF and saves them as PNG files.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    doc = fitz.open(pdf_path)
    image_count = 0

    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            image_filename = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_page{page_number+1}_img{img_index+1}.{image_ext}"
            image_filepath = os.path.join(output_dir, image_filename)

            with open(image_filepath, "wb") as img_file:
                img_file.write(image_bytes)

            image_count += 1
            print(f"Saved image: {image_filepath}")

    print(f"Total images extracted: {image_count}")
    doc.close()


if __name__ == "__main__":
    pdf_file = "/home/melahi/code/image-data/pdfs/02_AlloggioSaponaro.pdf"
    output_folder = "/home/melahi/code/image-data/output/"
    extract_images_from_pdf(pdf_file, output_folder)
