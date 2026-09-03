import tensorflow as tf
import numpy as np
import pytesseract
from PIL import Image
import json
import re

from extractor import (
    extract_aadhaar,
    extract_pan,
    extract_dl
)


# ============================================================
# 1. Configuration
# ============================================================

MODEL_PATH = "document_classifier_final.keras"

IMG_SIZE = (224, 224)

CLASS_NAMES = ["aadhar", "dl", "pan"]

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# ============================================================
# 2. Load classification model
# ============================================================

model = tf.keras.models.load_model(MODEL_PATH)


# ============================================================
# 3. Classify document
# ============================================================

def classify_document(image_path):

    image = tf.keras.utils.load_img(
        image_path,
        target_size=IMG_SIZE
    )

    image_array = tf.keras.utils.img_to_array(image)

    image_array = tf.expand_dims(
        image_array,
        axis=0
    )

    predictions = model.predict(
        image_array,
        verbose=0
    )

    predicted_index = np.argmax(predictions[0])

    document_type = CLASS_NAMES[predicted_index]

    confidence = float(
        predictions[0][predicted_index]
    )

    return document_type, confidence


# ============================================================
# 4. OCR
# ============================================================

def extract_text(image_path):

    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)

    return text


# ============================================================
# 5. Extract information based on document type
# ============================================================

def extract_information(document_type, text):

    if document_type == "aadhar":

        result = extract_aadhaar(text)

    elif document_type == "pan":

        result = extract_pan(text)

    elif document_type == "dl":

        result = extract_dl(text)

    else:

        result = {
            "document_type": "unknown",
            "name": "unknown",
            "dob": "unknown",
            "id_number": "unknown"
        }

    return result


# ============================================================
# 6. Complete pipeline
# ============================================================

def process_document(image_path):

    # -------------------------
    # Classification
    # -------------------------

    document_type, confidence = classify_document(
        image_path
    )

    print("\n========== CLASSIFICATION ==========")

    print("Document Type:", document_type)

    print(
        "Confidence:",
        round(confidence * 100, 2),
        "%"
    )


    # -------------------------
    # OCR
    # -------------------------

    text = extract_text(image_path)

    print("\n========== OCR TEXT ==========")

    print(text)


    # -------------------------
    # Information extraction
    # -------------------------

    result = extract_information(
        document_type,
        text
    )


    # Add classification confidence
    result["confidence"] = round(
        confidence * 100,
        2
    )


    return result


# ============================================================
# 7. Run program
# ============================================================

if __name__ == "__main__":

    image_path = "data/test/pan/pc8.jpg"

    result = process_document(image_path)

    print("\n========== FINAL JSON ==========")

    print(
        json.dumps(
            result,
            indent=4
        )
    )