import os
from PIL import Image

# Path to your image directory
image_dir = "/home/melahi/code/CLIP/images"

# Supported image extensions
valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')

# Loop through files in the directory
for filename in os.listdir(image_dir):
    if filename.lower().endswith(valid_extensions):
        filepath = os.path.join(image_dir, filename)
        try:
            with Image.open(filepath) as img:
                print(f"{filename}: size={img.size}, mode={img.mode}")
        except Exception as e:
            print(f"Failed to open {filename}: {e}")
