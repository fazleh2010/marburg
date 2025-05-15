import os
import numpy as np
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
import torch
from torchvision import models, transforms
import json
import numpy as np  # if your floats come from numpy

def load_images(image_dir, target_size=(224, 224)):
    images = []
    filenames = []
    for file in os.listdir(image_dir):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(image_dir, file)
            img = Image.open(path).convert("RGB").resize(target_size)
            images.append(img)
            filenames.append(file)
    return images, filenames

def extract_features(images):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    model = models.resnet18(pretrained=True)
    model = torch.nn.Sequential(*(list(model.children())[:-1]))  # remove classifier
    model.eval()

    features = []
    with torch.no_grad():
        for img in images:
            tensor = transform(img).unsqueeze(0)
            feature = model(tensor).squeeze().numpy()
            features.append(feature)
    return features

def find_similar_images(features, filenames, query_index=0, top_k=5):
    sims = cosine_similarity([features[query_index]], features)[0]
    sorted_indices = np.argsort(sims)[::-1][1:top_k + 1]  # skip query image itself
    return [(filenames[i], sims[i]) for i in sorted_indices]

# Convert numpy floats to Python floats
def convert_floats(obj):
    if isinstance(obj, dict):
        return {k: convert_floats(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_floats(v) for v in obj]
    elif isinstance(obj, np.floating):
        return float(obj)
    else:
        return obj

def main():
    image_dir = "/home/melahi/code/image-data/test_images/"  # <- Replace with your image folder
    query_index = 0                        # <- Replace with index of query image
    top_k = 5                              # <- How many similar images to return

    print("Loading images...")
    images, filenames = load_images(image_dir)

    if len(images) == 0:
        print("No images found in the directory.")
        return

    print("Extracting features...")
    features = extract_features(images)

    print(len("number of files:"+str(filenames)))

    similarity_data = {}
    for index, filename in enumerate(filenames):
        print(index, filename)
        #print(f"Finding top {top_k} similar images to: {filenames[query_index]}")
        similar_images = find_similar_images(features, filenames, query_index, top_k)
        query_index = query_index +1
        list={}
        for name, score in similar_images:
            #print(f"{name}: similarity = {score:.4f}")
            list[name]=str(score)
            similarity_data[filename]=list
    print(similarity_data)

    # Perform conversion
    #clean_data = convert_floats(similarity_data)

    # Save it to a JSON file
    with open(image_dir+"image_similarity_dict.json", "w") as f:
        json.dump(similarity_data, f, indent=4)
    #print(f"Finding top {top_k} similar images to: {filenames[query_index]}")
    #similar_images = find_similar_images(features, filenames, query_index, top_k)

    #for name, score in similar_images:
    #    print(f"{name}: similarity = {score:.4f}")

if __name__ == "__main__":
    main()
