import os
import torch
import csv
from PIL import Image
import clip

""" python -m clip.main """


def load_clip_model(device="cuda"):
    """Load the CLIP model and preprocessing function."""
    model, preprocess = clip.load("ViT-B/32", device=device)
    return model, preprocess


def read_text_file(file_path):
    """Read the text file and return a list of stripped lines."""
    with open(file_path, 'r') as file:
        texts = file.readlines()
    texts = [line.strip() for line in texts]
    return texts


def get_image_files(image_directory, valid_extensions):
    """Get all valid image file paths from the given directory."""
    image_files = []
    for filename in os.listdir(image_directory):
        if filename.lower().endswith(valid_extensions):
            filepath = os.path.join(image_directory, filename)
            try:
                with Image.open(filepath) as img:
                    # print(f"{filename}: size={img.size}, mode={img.mode}")
                    image_files.append(filepath)  # Store valid image paths
            except Exception as e:
                print(f"Failed to open {filename}: {e}")
    return image_files


def process_images_and_texts(image_files, texts, model, preprocess, device,output_dir):
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
                outputfile =output_dir+ os.path.basename(fileName)+".csv"
                with open(outputfile, "w", newline="") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerows(data)

    return probs

def calculate_percentage(total_value):
    return total_value * 100


def main():
    """Main function to load model, read text, and process images."""
    # Set device
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Load CLIP model
    model, preprocess = load_clip_model(device)

    # Define directories
    image_dir = "images/Sinti-und-Roma/"
    text_dir = "texts/"
    output_dir = "images/Sinti-und-Roma/output/"
    text_file = text_dir + "example.txt"



    # Supported image extensions
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')

    # Read texts from file
    texts = read_text_file(text_file)
    # print("Texts from file:", texts)

    # Get image files
    image_files = get_image_files(image_dir, valid_extensions)
    # print("images :", image_files)

    # Process images and texts, compute image-text similarities
    probs = process_images_and_texts(image_files, texts, model, preprocess, device,output_dir)


if __name__ == "__main__":
    main()
