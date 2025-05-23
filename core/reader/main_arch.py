import os
import fitz  # PyMuPDF


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


def read_all_pdfs_in_directory(directory):
    """
    Reads all PDF files in the specified directory and returns a dictionary
    with filenames as keys and text content as values.
    """
    pdf_texts = {}
    pdf_files = get_pdf_files(directory)

    for filepath in pdf_files:
        filename, text = read_pdf(filepath)
        pdf_texts[filename] = text

    return pdf_texts


# Example usage:
if __name__ == "__main__":
    folder_path = "/home/melahi/code/image-data"  # Replace with your folder path
    all_pdf_data = read_all_pdfs_in_directory(folder_path)

    for filename, content in all_pdf_data.items():
        print(f"\n=== {filename} ===\n{content[:500]}...")  # Print first 500 chars
