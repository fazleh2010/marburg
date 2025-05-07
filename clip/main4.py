import os
import torch
from PIL import Image
import clip


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
                    print(f"{filename}: size={img.size}, mode={img.mode}")
                    image_files.append(filepath)  # Store valid image paths
            except Exception as e:
                print(f"Failed to open {filename}: {e}")
    return image_files


def process_images_and_texts(image_files, texts, model, preprocess, device):
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
            for probList in probs:
                for prob in probList:
                    print(prob)
    return probs


def main():
    """Main function to load model, read text, and process images."""
    # Set device
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Load CLIP model
    model, preprocess = load_clip_model(device)

    # Define directories
    image_dir = "/home/melahi/code/marburg/private_images/"
    text_dir = "/home/melahi/code/marburg/texts/"
    text_file = text_dir + "example.txt"

    # Supported image extensions
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')

    # Read texts from file
    texts = read_text_file(text_file)
    print("Texts from file:", texts)

    # Get image files
    image_files = get_image_files(image_dir, valid_extensions)
    print("images :", image_files)

    # Process images and texts, compute image-text similarities
    probs = process_images_and_texts(image_files, texts, model, preprocess, device)

    print("Final texts:", texts)
    print("Probabilities:", probs)


if __name__ == "__main__":
    main()
