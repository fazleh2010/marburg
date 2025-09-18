import os
from PyPDF2 import PdfReader

# Set input/output folder
folder_path = "/home/melahi/code/Pietro/all-pdf-togather"

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(folder_path, filename)
        txt_filename = os.path.splitext(filename)[0] + ".txt"
        txt_path = os.path.join(folder_path, txt_filename)

        try:
            # Read the PDF
            with open(pdf_path, "rb") as f:
                reader = PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""

            # Write the extracted text to a .txt file
            with open(txt_path, "w", encoding="utf-8") as txt_file:
                txt_file.write(text)

            print(f"Extracted: {filename} → {txt_filename}")
        except Exception as e:
            print(f"Failed to process {filename}: {e}")
