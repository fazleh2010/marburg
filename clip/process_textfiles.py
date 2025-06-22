import csv
import os
from collections import defaultdict

def read_file_to_hashtable(file_path):
    """
    Reads a file line by line, splits each line at the first colon,
    and stores the key-value pairs in a dictionary.
    """
    hashtable = {}

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or ':' not in line:
                continue
            key, value = line.split(':', 1)
            hashtable[key.strip()] = value.strip()

    return hashtable


def write_hashtable_to_csv(hashtable, output_csv_path):
    """
    Writes key-value pairs from a dictionary to a CSV file.
    """
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Key", "Value"])  # Header
        for key, value in hashtable.items():
            writer.writerow([key, value])

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

def strip_extensions(filename):
    """
    Strips all extensions from a filename (e.g., 'file.jpeg.csv' -> 'file')
    """
    while '.' in filename:
        filename = filename.rsplit('.', 1)[0]
    return filename



def find_similar_named_files(directory):
    """
    Groups files that have the same base name (excluding all extensions).
    """
    file_groups = defaultdict(list)

    for file_name in os.listdir(directory):
        if valid_file(file_name):
           full_path = os.path.join(directory, file_name)
           if os.path.isfile(full_path):
              base_name = strip_extensions(file_name)
              file_groups[base_name].append(file_name)

    print("=== Files with same base name (partial match) ===")
    for base_name, files in file_groups.items():
        if len(files) > 1:
            print(f"\nGroup: {base_name}")
            index=1
            file1=""
            file2=""
            for file_path in files:
                print(str(index)+" -", file_path)
            first_file = directory+files[0]  # "file1.txt"
            second_file = directory+files[1]  # "file2.txt"
            print("First file:", first_file)
            print("Second file:", second_file)
            merge_two_csv_files(first_file, second_file, directory+base_name+"_merged_files.csv")


def valid_file(filename):
    # Exclude hidden, temp, and lock files
    exclude_prefixes = ('.', '~lock', '~$')
    return not filename.startswith(exclude_prefixes) and filename.endswith('.csv')


def process_all_txt_files(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt") and not filename.startswith("._"):
            txt_path = os.path.join(input_dir, filename)
            csv_path = os.path.join(output_dir, filename.replace(".txt", ".csv"))

            print(f"📄 Processing: {txt_path}")
            hashtable = read_file_to_hashtable(txt_path)
            write_hashtable_to_csv(hashtable, csv_path)
            print(f"✅ Saved CSV: {csv_path}")
        else:
            print(f"⚠️ Skipping file: {filename}")


def main():
    input_dir="/home/melahi/code/marburg/images/Sinti-und-Roma/"
    output_dir="/home/melahi/code/marburg/images/Sinti-und-Roma/output/"
    process_all_txt_files(input_dir, output_dir)

    find_similar_named_files(output_dir)



if __name__ == "__main__":
    main()
