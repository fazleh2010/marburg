from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PIL import Image

def add_images_to_pdf(image_files, output_path="output_reportlab.pdf"):
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

def main():
    image_dir = '/home/melahi/code/image-data/extracted_images/'  # Change this to your file path
    output_dir = '/home/melahi/code/image-data/output/'  # Change this to your file path

    file_path = image_dir + 'record.txt'
    image_files = [
        image_dir+ "02_AlloggioSaponaro_page7_img1.jpeg",
        image_dir+"02_AlloggioSaponaro_page7_img2.jpeg",
        image_dir+"02_AlloggioSaponaro_page7_img3.jpeg"
    ]
    add_images_to_pdf(image_files, output_path=output_dir+"output_reportlab.pdf")


if __name__ == "__main__":
    main()
