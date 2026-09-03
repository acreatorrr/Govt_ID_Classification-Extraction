# Indian ID Document Recognition & Information Extraction

An AI-based document processing pipeline for classifying Indian identity documents and extracting key information using Deep Learning and OCR.

## Overview

This project implements an end-to-end pipeline that:

1. Accepts an ID document image as input.
2. Classifies the document into:

   * Aadhaar
   * PAN Card
   * Driving Licence
3. Extracts text from the document using Tesseract OCR.
4. Extracts relevant information based on the predicted document type.
5. Returns the extracted information as structured JSON.

## Pipeline

```text
Input Image
     │
     ▼
EfficientNetB0
     │
     ▼
Document Classification
     │
     ├── Aadhaar
     ├── PAN
     └── Driving Licence
     │
     ▼
Tesseract OCR
     │
     ▼
Document-Specific Information Extraction
     │
     ├── Name
     ├── Date of Birth
     └── Document Number
     │
     ▼
Structured JSON Output
```

## Technologies Used

* Python
* TensorFlow / Keras
* EfficientNetB0
* Tesseract OCR
* Pytesseract
* Pillow
* Regular Expressions

## Project Structure

```text
id_recognition/
│
├── data/
│   ├── train/
│   │   ├── aadhar/
│   │   ├── pan/
│   │   └── dl/
│   │
│   └── test/
│       ├── aadhar/
│       ├── pan/
│       └── dl/
│
├── train.py
├── predict.py
├── predict_demo.py
├── ocr.py
├── extractor.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Dataset

For development and evaluation, the dataset contains three document classes:

* Aadhaar
* PAN
* Driving Licence

The dataset is divided into training and testing sets.

For the current prototype:

* 16 training images per class
* 2 testing images per class

The dataset is intentionally kept small because this project focuses on demonstrating the complete document AI pipeline rather than achieving production-level classification accuracy.

> Note: Real personal identity documents should not be uploaded to the repository. Use public, synthetic, or appropriately redacted samples for development and testing.

## Model

The document classifier uses **EfficientNetB0 pretrained on ImageNet** with transfer learning.

Input images are resized to:

```text
224 × 224
```

Data augmentation is applied during training using:

* Random Rotation
* Random Zoom
* Random Contrast

The model is trained to classify the three document categories.

## OCR

Tesseract OCR is used to extract text from the classified document.

The OCR output is then passed to a document-specific extraction function.

## Information Extraction

Different extraction rules are applied depending on the predicted document type.

### Aadhaar

Extracts:

```json
{
    "document_type": "aadhar",
    "name": "Example Name",
    "dob": "DD/MM/YYYY",
    "aadhaar_number": "XXXX XXXX XXXX"
}
```

### PAN

Extracts:

```json
{
    "document_type": "pan",
    "name": "Example Name",
    "dob": "DD/MM/YYYY",
    "pan_number": "ABCDE1234F"
}
```

### Driving Licence

Extracts:

```json
{
    "document_type": "dl",
    "name": "Example Name",
    "dob": "DD/MM/YYYY",
    "dl_number": "XX-XX-XXXXXXXXXXX"
}
```

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd id_recognition
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Tesseract OCR

Tesseract OCR must be installed separately because `pytesseract` is a Python wrapper around the Tesseract OCR engine.

On Windows, install Tesseract and update the executable path in the Python code if necessary.

Example:

```python
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
```

## Training the Model

Place the training images inside:

```text
data/train/
```

with the following structure:

```text
data/train/
├── aadhar/
├── pan/
└── dl/
```

Then run:

```bash
python train.py
```

This trains the EfficientNet-based document classifier.

## Testing Classification

Place test images inside:

```text
data/test/
```

Then run:

```bash
python predict.py
```

This displays the actual document class, predicted class, and prediction confidence.

## Running the Complete Pipeline

Run:

```bash
python main.py
```

The pipeline performs:

```text
Image
→ Classification
→ OCR
→ Information Extraction
→ JSON
```

Example output:

```json
{
    "document_type": "pan",
    "name": "Example Name",
    "dob": "31/01/2001",
    "pan_number": "ABCDE1234F",
    "confidence": 71.89
}
```

## Design Considerations

The project is designed as a lightweight prototype demonstrating an end-to-end document intelligence workflow.

The classification stage determines which extraction strategy should be used. This allows the extraction logic to be document-specific instead of applying the same rules to every document.

OCR output can contain noise or incorrectly recognized characters. Therefore, regular expressions, label-based extraction, and simple validation rules are used to improve the reliability of the extracted fields.

## Limitations

This is a prototype and is not intended for production use.

Current limitations include:

* Small training dataset
* OCR errors on low-quality images
* Rule-based information extraction
* Limited document layout variations
* Classification confidence may vary depending on image quality
* No production-grade PII/security handling

For production deployment, the system could be improved using a larger and more diverse dataset, document layout analysis, advanced OCR, Named Entity Recognition, confidence thresholds, and stronger validation.

## Future Improvements

Potential improvements include:

* Increase training dataset size
* Add more document layouts and image variations
* Improve OCR preprocessing
* Add an `unknown` document class
* Introduce confidence thresholds
* Use layout-aware document understanding models
* Improve entity extraction using NER or transformer-based models
* Build a REST API using FastAPI
* Add a Streamlit interface
* Add automated testing
* Containerize the application using Docker

## Disclaimer

This project is developed for educational and assessment purposes. It should not be used for processing real identity documents in a production environment without appropriate privacy, security, compliance, and data-protection controls.
