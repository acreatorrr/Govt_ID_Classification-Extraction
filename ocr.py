import pytesseract
from PIL import Image


# Tell Python where Tesseract is installed
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# Test image
image_path = "data/test/pan/pc8.jpg"


# Open image
image = Image.open(image_path)


# Run OCR
text = pytesseract.image_to_string(image)


# Display result
print("========== OCR OUTPUT ==========")
print(text)