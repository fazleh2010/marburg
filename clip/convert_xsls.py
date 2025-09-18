import pandas as pd
from openpyxl import Workbook
from openpyxl.drawing.image import Image
import csv
import os


def paste_image_to_excel(image_path, excel_output):
    """
    Inserts an image into an Excel sheet and saves the file.

    :param image_path: Path to the image file to insert
    :param excel_output: Path for the output Excel file
    """
    try:
        # Create a new Excel workbook and select the active sheet
        workbook = Workbook()
        sheet = workbook.active

        # Load the image
        img = Image(image_path)

        # Paste the image at the specified cell
        sheet.add_image(img, 'B2')  # Adjust the cell if needed

        # Save the workbook
        workbook.save(excel_output)

        print(f"Image successfully pasted into {excel_output}")
    except Exception as e:
        print(f"An error occurred: {e}")

def convert_csv_to_excel(csv_file, excel_file):
    """
    Converts a CSV file to an Excel file.

    :param csv_file: Path to the input CSV file
    :param excel_file: Path to the output Excel file
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(csv_file)

        # Save the DataFrame to an Excel file
        df.to_excel(excel_file, index=False)

        print(f"File successfully converted to {excel_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

def merge_two_csv_files(file1, file2, output_file):
    """
    Merges two CSV files into a single CSV file.
    Assumes both files have the same header structure.
    """
    with open(output_file, 'w', newline='', encoding='utf-8') as fout:
        writer = None

        for i, file in enumerate([file1, file2]):
            with open(file, 'r', encoding='utf-8') as fin:
                reader = csv.reader(fin)
                header = next(reader)

                if writer is None:
                    writer = csv.writer(fout)
                    writer.writerow(header)  # write header only once

                for row in reader:
                    writer.writerow(row)

    print(f"✅ Merged CSV written to: {output_file}")

def main():
    input_dir="/home/melahi/code/marburg/images/Zigeuner/FOTO/"

    #image_path = input_dir + 'Messerschmidt_Franz_Xaver_Der_erboste_und_rachgierige_Zigeuner_Wien_ede394e0.jpeg'  # Replace with your image file path
    #image_excel_file =input_dir+ 'Messerschmidt_Franz_Xaver_Der_erboste_und_rachgierige_Zigeuner_Wien_ede394e0_image.xlsx'  # Desired Excel file name
    #paste_image_to_excel(image_path, image_excel_file)

    #csv_file = input_dir+'Messerschmidt_Franz_Xaver_Der_erboste_und_rachgierige_Zigeuner_Wien_ede394e0_merged_files.csv'  # Replace with your CSV file name
    #data_excel_file =input_dir+ 'Messerschmidt_Franz_Xaver_Der_erboste_und_rachgierige_Zigeuner_Wien_ede394e0_merged_files.xlsx'  # Desired Excel file name
    #convert_csv_to_excel(csv_file, data_excel_file)

    for filename in os.listdir(input_dir):
        if filename.endswith('.csv'):
            csv_path = os.path.join(input_dir, filename)
            xlsx_filename = filename.replace('.csv', '.xlsx')
            xlsx_path = os.path.join(input_dir, xlsx_filename)

            # Read CSV file
            df = pd.read_csv(csv_path)

            # Write to Excel file
            df.to_excel(xlsx_path, index=False)
            print(f"Converted: {filename} -> {xlsx_filename}")

    print("All CSV files have been converted to XLSX.")

    #output_file=input_dir+ 'Leonardo_da_Vinci_Fuenf_groteske_Kopfstudien_Mann_wird_von_Zigeunern_3377131a_final_files.xlsx'
    # marge files
    # merge_two_csv_files(image_excel_file, data_excel_file, output_file)


if __name__ == '__main__':
    main()
