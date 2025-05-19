from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from PIL import Image

def add_images_with_titles_to_pdf(image_title_list, output_path="output.pdf"):
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
    # List of (image_path, title)

    image_dir = '/home/melahi/code/image-data/extracted_images/'  # Change this to your file path
    output_dir = '/home/melahi/code/image-data/output/'  # Change this to your file path

    image_files = [
        image_dir + "02_AlloggioSaponaro_page7_img1.jpeg",
        image_dir + "02_AlloggioSaponaro_page7_img2.jpeg",
        image_dir + "02_AlloggioSaponaro_page7_img3.jpeg"
    ]

    images_with_titles = [
        (image_dir + "02_AlloggioSaponaro_page7_img1.jpeg", "02_AlloggioSaponaro_page7"),
        (image_dir + "02_AlloggioSaponaro_page7_img2.jpeg", "02_AlloggioSaponaro_page7"),
        (image_dir + "02_AlloggioSaponaro_page7_img3.jpeg", "02_AlloggioSaponaro_page7")
    ]

    add_images_with_titles_to_pdf(images_with_titles, output_path=output_dir+"images_with_titles.pdf")

if __name__ == "__main__":
    main()
