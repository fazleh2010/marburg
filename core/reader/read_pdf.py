import os
import fitz  # PyMuPDF
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

def extract_text_by_page(doc):
    """
    Extracts text from each page and returns a dictionary: {page_number: text}.
    """
    page_texts = {}
    for page_num in range(len(doc)):
        try:
            page = doc.load_page(page_num)
            text = page.get_text()
            page_texts[str(page_num + 1)] = text  # Store page numbers as strings
        except Exception as e:
            print(f"Error reading page {page_num}: {e}")
            page_texts[str(page_num + 1)] = ""
    return page_texts

def read_pdf_by_page(filepath):
    """
    Reads a PDF file and returns a dict {filename: {page_number: text}}.
    """
    doc = open_pdf(filepath)
    filename = os.path.basename(filepath)
    if doc:
        page_texts = extract_text_by_page(doc)
        doc.close()
        return filename, page_texts
    return filename, {}

def read_all_pdfs_to_json_by_page(directory, output_json_path):
    """
    Reads all PDFs and saves per-page text content to a JSON file.
    """
    pdf_data = {}
    pdf_files = get_pdf_files(directory)

    for filepath in pdf_files:
        filename, page_texts = read_pdf_by_page(filepath)
        pdf_data[filename] = page_texts

    try:
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(pdf_data, f, ensure_ascii=False, indent=2)
        print(f"Saved page-level text to {output_json_path}")
    except Exception as e:
        print(f"Error writing JSON file: {e}")

# Example usage:
if __name__ == "__main__":
    folder_path_input = "/home/melahi/code/image-data/pdfs/"  # Replace with your path
    folder_path_output = "/home/melahi/code/image-data/output/"  # Replace with your path
    output_file = "pdf_texts.json"
    read_all_pdfs_to_json_by_page(folder_path_input, folder_path_output + output_file)