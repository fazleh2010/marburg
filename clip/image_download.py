import requests


def read_text_file(file_path):
    """Read the text file and return a list of stripped lines."""
    with open(file_path, 'r') as file:
        texts = file.readlines()
    texts = [line.strip() for line in texts]
    return texts


def download_image(image_url, save_path):
    response = requests.get(image_url)

    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Image saved to {save_path}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")


# Example usage
image_dir = "/home/melahi/code/marburg/images/"
text_dir = "/home/melahi/code/marburg/texts/"
text_file = text_dir + "image_links.txt"

url_text_files = read_text_file(text_file)
index=1

for image_url in url_text_files:
    print("image_url:", image_url)
    filename=str(index)+"_painting"+".png"
    download_image(image_url, image_dir+filename)
    index=index+1
