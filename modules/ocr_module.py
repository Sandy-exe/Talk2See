import pytesseract

def get_OCR(image):
    try:
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(e)
        return "Error"
