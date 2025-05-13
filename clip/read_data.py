import json
import langcodes

def read_language_from_json(json_path,lang_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    languages = []
    my_hash = {}
    english_files=0
    german_files=0
    french_files=0
    italian_files =0
    unknown_files=0

    for file_name, pages in data.items():
        #print(f"\n File: {file_name}")
        file_language=""
        for page_number, page_data in pages.items():
            text = page_data.get("text", "")
            code = page_data.get("language", "unknown")
            if code == 'unknown':
                name = 'Unknown Language'
            else:
                name = langcodes.get(code).language_name()
            file_language = name

            images = page_data.get("images", [])
            #print(f"\n  Page: {page_number}")
            #print(f"   Language: {language}")
            #print(f"   Text: {text[:200]}...")  # Show first 200 characters
            #print(f"   Images:")
            #if images:
            #    for i, img in enumerate(images, 1):
            #        print(f"    - Image {i}: {img}")
            #else:
            #    print("    - None")
        languages.append(file_language)
        my_hash[file_name] = file_language
        if file_language == 'English':
            english_files = english_files + 1
        elif file_language == 'German':
            german_files = german_files + 1
        elif file_language == 'French':
            french_files = french_files +1
        elif file_language == 'Italian':
            italian_files = italian_files + 1
        elif file_language == 'Unknown Language':
            unknown_files = unknown_files + 1

        #print(f"\n File: {file_name}"+" language::"+file_language)
    language_codes = set(languages)
    print(language_codes)
    print("english files::"+str(english_files)+ " german_files::" + str(german_files)
          +" french_files::"+str(french_files)
          +" italian_files::" + str(italian_files)
          +" unknown_files::" + str(unknown_files))

    with open(lang_path, "w") as f:
        json.dump(my_hash, f, indent=2)

def main():
    json_path = "/home/melahi/code/image-data/output/pdf_data.json"  # Replace with your actual path
    lang_path = "/home/melahi/code/image-data/output/file_language.json"  # Replace with your actual path
    read_language_from_json(json_path,lang_path)

if __name__ == "__main__":
    main()
