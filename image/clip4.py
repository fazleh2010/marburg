import os
import torch
import csv
from PIL import Image
import clip
import json
import nltk
from nltk.corpus import stopwords
import re
from nltk.corpus import stopwords
import numpy as np

# Download stopwords (only the first time)
nltk.download("stopwords")
STOPWORDS = set(stopwords.words("english"))

def clean_text(text):
    """
    Remove stopwords, punctuation, and extra whitespace from a string.
    """
    # Lowercase
    text = text.lower()

    # Remove all non-alphanumeric characters (punctuation, symbols)
    text = re.sub(r'[^a-z0-9\s]', '', text)

    # Split into words and remove stopwords
    tokens = text.split()
    filtered = [word for word in tokens if word not in STOPWORDS]

    # Join back into string
    return " ".join(filtered)

def load_clip_model(device="cuda"):
    """Load the CLIP model and preprocessing function."""
    model, preprocess = clip.load("ViT-B/32", device=device)
    return model, preprocess


def clean_text(sentence):
    """Remove stopwords from a sentence."""
    tokens = sentence.split()
    filtered = [w for w in tokens if w.lower() not in STOPWORDS]
    return " ".join(filtered)


def get_image_files(image_directory, valid_extensions):
    """Get all valid image file paths from the given directory."""
    image_files = []
    for filename in os.listdir(image_directory):
        if filename.lower().endswith(valid_extensions):
            filepath = os.path.join(image_directory, filename)
            try:
                with Image.open(filepath) as img:
                    image_files.append(filepath)
            except Exception as e:
                print(f"⚠️ Failed to open {filename}: {e}")
    return image_files


def tokenize_with_truncate(texts, device):
    """
    Tokenize texts safely by truncating them if they exceed CLIP's max length (77 tokens).
    """
    tokenized = []
    valid_texts = []
    for t in texts:
        cleaned = clean_text(t)
        tokens = clip.tokenize([cleaned], truncate=True)  # auto-truncate
        tokenized.append(tokens[0])
        valid_texts.append(cleaned)
    return torch.stack(tokenized).to(device), valid_texts


def process_images_and_texts(image_files, texts, model, preprocess, device, output_dir):
    """Process the images and texts, compute image-text similarities."""
    for fileName in image_files:
        print(f"Processing: {fileName}")
        image = preprocess(Image.open(fileName)).unsqueeze(0).to(device)

        # Tokenize after cleaning
        text, valid_texts = tokenize_with_truncate(texts, device)

        with torch.no_grad():
            image_features = model.encode_image(image)
            text_features = model.encode_text(text)

            logits_per_image, logits_per_text = model(image, text)
            probs = logits_per_image.softmax(dim=-1).cpu().numpy()

            for probList in probs:
                data = []
                for idx, prob in enumerate(probList):
                    data.append([valid_texts[idx], prob])

                # Sort descending
                data.sort(key=lambda x: x[1], reverse=True)

                # Print top results
                for item in data[:10]:
                    print(f"{item[0]}\t{item[1]}")

                # Save all results
                outputfile = os.path.join(output_dir, os.path.basename(fileName) + ".csv")
                with open(outputfile, "w", newline="") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerows(data)

    return probs

def text_to_list(textsString):
    texts = textsString.split()
    unique_words = list(set(texts))
    return unique_words


def process_images_and_texts(image_files, texts, model, preprocess, device,output_dir,page_num,para_index,original_para):
    """Process the images and texts, compute image-text similarities."""
    for fileName in image_files:
        print(f"Processing: {fileName}")
        image = preprocess(Image.open(fileName)).unsqueeze(0).to(device)
        text = clip.tokenize(texts).to(device)

        with torch.no_grad():
            # Compute features
            image_features = model.encode_image(image)
            text_features = model.encode_text(text)

            # Compute logits and probabilities
            logits_per_image, logits_per_text = model(image, text)
            probs = logits_per_image.softmax(dim=-1).cpu().numpy()

            # Print probabilities
            index=0
            content=""
            for probList in probs:
                print("texts_size:"+str(len(texts))+" probabiltyList:"+str(len(probList)))
                data = []
                probabilityValue = {}
                for prob in probList:
                    # print(str(index)+":"+texts[index]+":"+str(calculate_percentage(prob)))
                    #line=str(index)+","+texts[index]+","+str(prob)+"\n"
                    data.append([texts[index], prob])
                    #content+=line
                    index=index+1
                # Write to a CSV file
                data.sort(key=lambda x: x[1], reverse=True)
                for item in data:
                    print(f"{item[0]}\t{item[1]}")
                    key = item[0]
                    value = item[1]
                    probabilityValue[key] = value  # add to the map

                #outputfile =output_dir+ os.path.basename(fileName)+"_"+"pagenumber-"+str(page_num)+"_"+"paragraph-"+str(para_index)+"_"+".csv"
                #with open(outputfile, "w", newline="") as csv_file:
                    #    writer = csv.writer(csv_file)
                    #    writer.writerows(data)

    return fileName, probabilityValue

# Custom encoder to handle numpy arrays & scalars
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()              # convert arrays to list
        if isinstance(obj, (np.generic,)):
            return obj.item()                # convert scalars (e.g. float32 → float)
        return super().default(obj)


def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = load_clip_model(device)

    base_dir = "/home/melahi/code/documents/"
    image_dir = os.path.join(base_dir, "extracted_images_test")
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')

    # Step 1: find all json files
    json_files = [f for f in os.listdir(image_dir) if f.endswith(".json")]

    for json_file in json_files:
        prefix = os.path.splitext(json_file)[0]
        json_path = os.path.join(image_dir, json_file)

        print(f"\n🔎 Processing prefix: {prefix}")

        # Step 2: get matching images
        image_files = [
            os.path.join(image_dir, f) for f in os.listdir(image_dir)
            if f.startswith(prefix) and f.lower().endswith(valid_extensions)
        ]

        if not image_files:
            print(f"⚠️ No images found for prefix {prefix}, skipping...")
            continue

        # Step 3: load json data
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        final_results = []

        for page in data:
            page_num = page.get("page")
            paragraphs = page.get("paragraphs", [])

            for para_index, para in enumerate(paragraphs, start=1):
                original_para = para
                para = re.sub(r'\s+', ' ', para)  # collapse whitespace
                para = re.sub(r'[^a-zA-Z0-9\s]', '', para)
                para = re.sub(r'\d+', '', para)
                para = " ".join([word for word in para.split() if len(word) > 2])
                para = clean_text(para)
                texts = text_to_list(para)

                print(f"\n=== {prefix} | Page {page_num}, Paragraph {para_index} ===")

                fileName, probabilityValue = process_images_and_texts(
                    image_files, texts, model, preprocess, device,
                    output_dir, page_num, para_index, original_para
                )

                final_results.append({
                    "image": fileName,
                    "page": page_num,
                    "paragraph_number": para_index,
                    "original_text": original_para,
                    "results": probabilityValue
                })

        # Step 4: write results
        output_json = os.path.join(output_dir, f"{prefix}_results.json")
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(final_results, f, indent=2, ensure_ascii=False, cls=NumpyEncoder)

        print(f"✅ Results saved: {output_json}")



if __name__ == "__main__":
    main()
