import os
import fitz  # from PyMuPDF
import json


def get_pdf_files(directory):
    """
    Returns a list of full file paths to all PDF files in the given directory.
    """
    return [
        os.path.join(directory, filename)
        for filename in os.listdir(directory)
        if filename.lower().endswith('.pdf')
    ]


def open_pdf(filepath):
    """
    Opens a PDF file and returns the document object.
    """
    try:
        return fitz.open(filepath)
    except Exception as e:
        print(f"Error opening {filepath}: {e}")
        return None


def extract_all_text(doc):
    """
    Extracts text from all pages of the PDF document.
    """
    full_text = ""
    for page_num in range(len(doc)):
        try:
            page = doc.load_page(page_num)
            text = page.get_text()
            full_text += f"\n--- Page {page_num + 1} ---\n{text}"
        except Exception as e:
            print(f"Error reading page {page_num} in document: {e}")
    return full_text


def read_pdf(filepath):
    """
    Reads the entire text content from a single PDF file.
    Returns the file name and extracted text.
    """
    doc = open_pdf(filepath)
    if doc:
        text = extract_all_text(doc)
        doc.close()
        return os.path.basename(filepath), text
    return os.path.basename(filepath), ""


def read_all_pdfs_to_json(directory, output_json_path):
    """
    Reads all PDFs in the given directory and stores their text content
    in a JSON file with the filename as the key.
    """
    pdf_data = {}
    pdf_files = get_pdf_files(directory)

    for filepath in pdf_files:
        filename, text = read_pdf(filepath)
        pdf_data[filename] = text

    # Save to JSON
    try:
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(pdf_data, f, ensure_ascii=False, indent=2)
        print(f"Saved extracted text to {output_json_path}")
    except Exception as e:
        print(f"Error writing JSON file: {e}")


# Example usage:
if __name__ == "__main__":
    folder_path_input = "/home/melahi/code/image-data/pdfs/"  # Replace with your path
    folder_path_output = "/home/melahi/code/image-data/output/"  # Replace with your path
    output_file = "pdf_texts.json"
    read_all_pdfs_to_json(folder_path_input, folder_path_output+output_file)
