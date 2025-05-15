import json

def read_records_from_file(file_path):
    records = []
    current_record = []
    in_record = False

    with open(file_path, 'r') as file:
        for line in file:
            line = line.rstrip('\n')
            line = line.lstrip()
            if line.startswith("Record number :"):
                if in_record and current_record:
                    records.append('\n'.join(current_record))
                    current_record = []
                in_record = True
                current_record.append(line)
            elif line.startswith("IN:") and in_record:
                current_record.append(line)
                records.append('\n'.join(current_record))
                current_record = []
                in_record = False
            elif in_record:
                current_record.append(line)

    return records


def main():
    directory = '/home/melahi/code/image-data/output/'  # Change this to your file path
    file_path = directory + 'record.txt'
    output_json = directory + 'json_records.json'
    #file_path = '/home/melahi/code/image-data/output/record.txt'  # Change this to your file path
    all_records = read_records_from_file(file_path)

    # Print each record
    first_5 = []
    index = 0
    for i, record in enumerate(all_records, 1):
        print(f"--- Record {i} ---\n{record}\n")
        first_5.append(record)

    # print(first_5)
    # Save to JSON
    #with open(output_json, 'w') as json_file:
    #    json.dump(first_5, json_file, indent=4)

    #print(f"\nFirst 5 records saved to '{output_json}'")

if __name__ == '__main__':
    main()
