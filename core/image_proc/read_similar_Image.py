from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from PIL import Image
import json


def add_images_to_pdf(image_files, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    page_width, page_height = A4

    for image_path in image_files:
        img = Image.open(image_path)
        img_width, img_height = img.size

        scale = min(page_width / img_width, page_height / img_height)
        width = img_width * scale
        height = img_height * scale

        x = (page_width - width) / 2
        y = (page_height - height) / 2

        c.drawImage(image_path, x, y, width, height)
        c.showPage()

    c.save()

def add_images_with_titles_to_pdf(image_title_list, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    page_width, page_height = A4

    for image_path, title in image_title_list:
        # Open the image
        img = Image.open(image_path)
        img_width, img_height = img.size

        # Convert image dimensions from pixels to mm (approx. 0.264583 mm per pixel)
        img_width_mm = img_width * 0.264583
        img_height_mm = img_height * 0.264583

        # Scale to fit within page
        max_width = page_width - 40 * mm  # padding
        max_height = page_height - 60 * mm  # leave space for title
        scale = min(max_width / img_width_mm, max_height / img_height_mm)

        display_width = img_width_mm * scale
        display_height = img_height_mm * scale

        # Compute position (centered)
        x = (page_width - display_width) / 2
        y = (page_height - display_height) / 2 - 10 * mm  # lower to leave room for title

        # Draw title
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(page_width / 2, y + display_height + 20, title)

        # Draw image
        c.drawImage(image_path, x, y, width=display_width, height=display_height)

        c.showPage()

    c.save()


def main():
    # Replace this with loading from a file using json.load()

    image_dir = '/home/melahi/code/image-data/extracted_images/'  # Change this to your file path
    output_dir = '/home/melahi/code/image-data/output/'  # Change this to your file path
    similiar_dir = '/home/melahi/code/image-data/output/similar_dir/'  # Change this to your file path



    with open(output_dir+"image_similarity_dict.json", "r") as f:
        data = json.load(f)


    # images_with_titles={}
    selected_images=["Davanti_alla_Resurrezione_di_Cristo_di_P",
                     "La_Presentazione_al_Tempio_attribuita_a_page6",
                     "PIERO_DELLA_FRANCESCAS_BAPTISM_OF_CHRIST",
                     "Concordia_in_Piero_della_Francescas_Bapt_page10_img1.jpeg"]

    # Example: print all keys and values
    count=0
    for base_image, matches in data.items():
        #if "Concordia_in_Piero_della_Francescas_Bapt_page10_img1.jpeg" not in base_image:
        #   continue
        image_files=[]
        print("count::"+str(count)+" "+f"Base image: {image_dir+base_image}")
        base_image_name=base_image.replace(".jpeg","")
        # images_with_titles [image_dir+base_image]= base_image_name
        image_files.append(image_dir+base_image)
        count=count+1
        for matched_image, score in matches.items():
            print(f"  → Match: {image_dir+matched_image}, Score: {score}")
            # images_with_titles[image_dir+matched_image] = matched_image.replace(".jpeg", "")
            image_files.append(image_dir+matched_image)
        # print(image_files)
        output_path = similiar_dir + "output_"+base_image_name+".pdf"
        add_images_to_pdf(image_files, output_path)
    print(count)  # 22,525 images

if __name__ == "__main__":
    main()
