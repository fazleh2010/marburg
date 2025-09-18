from openpyxl import Workbook
from openpyxl.drawing.image import Image

# Create a new Excel workbook and select the active sheet
workbook = Workbook()
sheet = workbook.active

# Load the image you want to paste
image_path = 'your_image.png'  # Change this to your image file path
img = Image(image_path)

# Specify the position (cell) where you want to paste the image
sheet.add_image(img, 'B2')  # 'B2' is the top-left corner of the image placement

# Save the workbook
workbook.save('image_in_excel.xlsx')

print("Image successfully pasted into Excel file.")
