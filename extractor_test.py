import re


def extract_aadhaar(text):

    # -----------------------------
    # Extract Aadhaar number
    # -----------------------------
    aadhaar_match = re.search(
        r"\b\d{4}\s\d{4}\s\d{4}\b",
        text
    )

    if aadhaar_match:
        aadhaar_number = aadhaar_match.group()
    else:
        aadhaar_number = "unknown"


    # -----------------------------
    # Extract Date of Birth
    # -----------------------------
    dob_match = re.search(
        r"\b\d{2}[-/]\d{2}[-/]\d{4}\b",
        text
    )

    if dob_match:
        dob = dob_match.group()
    else:
        dob = "unknown"

    # -----------------------------
    # Extract Name
    # -----------------------------
    lines = text.splitlines()

    name = "unknown"

    skip_words = [
        "GOVERNMENT OF INDIA",
        "GOVT OF INDIA",
        "GOVT. OF INDIA",
        "MY AADHAAR",
        "MALE",
        "FEMALE",
        "DOB",
        "DATE OF BIRTH",
        "VID",
        "ISSUE DATE"
    ]

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Remove OCR special characters
        clean_line = re.sub(r"[^A-Za-z ]", "", line)
        clean_line = re.sub(r"\s+", " ", clean_line).strip()

        if not clean_line:
            continue

        # Skip known labels
        if clean_line.upper() in skip_words:
            continue

        # Skip lines containing DOB
        if re.search(r"\d{2}[-/]\d{2}[-/]\d{4}", line):
            continue

        # Skip Aadhaar number
        if re.fullmatch(r"\d{4}\s\d{4}\s\d{4}", line):
            continue

        # Possible name
        words = clean_line.split()

        if (
                len(words) >= 2
                and all(word.isalpha() for word in words)
                and all(len(word) >= 2 for word in words)
        ):
            name = clean_line
            break

    return {
        "document_type": "aadhar",
        "name": name,
        "dob": dob,
        "aadhaar_number": aadhaar_number
    }

# -----------------------------
# Test
# -----------------------------

if __name__ == "__main__":

    sample_text = """
    GOVERNMENT OF INDIA

    SAMARTH SHARMA
    Male
    20-06-1986

    1234 5678 9012
    MY AADHAAR
    """

    result = extract_aadhaar(sample_text)

    print(result)




def extract_pan(text):

    # -----------------------------
    # Extract PAN number
    # -----------------------------
    pan_match = re.search(
        r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
        text.upper()
    )

    if pan_match:
        pan_number = pan_match.group()
    else:
        pan_number = "unknown"


    # -----------------------------
    # Extract Date of Birth
    # -----------------------------
    dob_match = re.search(
        r"\b\d{2}[-/]\d{2}[-/]\d{4}\b",
        text
    )

    if dob_match:
        dob = dob_match.group()
    else:
        dob = "unknown"

    # -----------------------------
    # Extract Name
    # -----------------------------
    lines = text.splitlines()

    name = "unknown"

    skip_words = [
        "INCOME TAX DEPARTMENT",
        "GOVT. OF INDIA",
        "GOVT OF INDIA",
        "GOVERNMENT OF INDIA",
        "PERMANENT ACCOUNT NUMBER",
        "PERMANENT ACCOUNT NUMBER CARD",
        "SIGNATURE",
        "DATE OF BIRTH",
        "FATHER NAME",
        "FATHER'S NAME",
        "NAME",
    ]

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Remove OCR special characters
        clean_line = re.sub(r"[^A-Za-z ]", "", line)
        clean_line = re.sub(r"\s+", " ", clean_line).strip()

        if not clean_line:
            continue

        # Skip common PAN text
        if clean_line.upper() in skip_words:
            continue

        # Skip PAN number
        if re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", clean_line.upper()):
            continue

        # Skip DOB
        if re.fullmatch(r"\d{2}[-/]\d{2}[-/]\d{4}", line):
            continue

        # Possible name
        words = clean_line.split()

        if (
                len(words) >= 2
                and all(word.isalpha() for word in words)
                and all(len(word) >= 2 for word in words)
        ):
            name = clean_line
            break

    return {
        "document_type": "pan",
        "name": name,
        "dob": dob,
        "pan_number": pan_number
    }

if __name__ == "__main__":

    sample_text = """
    INCOME TAX DEPARTMENT
    GOVERNMENT OF INDIA

    SAMARTH SHARMA

    Date of Birth
    20-06-1986

    ABCDE1234F
    """

    result = extract_pan(sample_text)

    print(result)



def extract_dl(text):

    # -----------------------------
    # Extract Driving Licence number
    # -----------------------------
    dl_patterns = [
        r"\b[A-Z]{2}[- ]?[0-9]{2}[- ]?[0-9]{4,11}\b",
        r"\b[A-Z]{2}[0-9]{2}[0-9]{4,11}\b"
    ]

    dl_number = "unknown"

    for pattern in dl_patterns:

        match = re.search(pattern, text.upper())

        if match:
            dl_number = match.group()
            break


    # -----------------------------
    # Extract Date of Birth
    # -----------------------------
    dob_match = re.search(
        r"\b\d{2}[-/]\d{2}[-/]\d{4}\b",
        text
    )

    if dob_match:
        dob = dob_match.group()
    else:
        dob = "unknown"

    # -----------------------------
    # Extract Name
    # -----------------------------
    lines = text.splitlines()

    name = "unknown"

    skip_words = [
        "DRIVING LICENCE",
        "DRIVING LICENSE",
        "LICENCE",
        "LICENSE",
        "GOVERNMENT OF INDIA",
        "GOVT OF INDIA",
        "GOVT. OF INDIA",
        "TRANSPORT",
        "DEPARTMENT",
        "DATE OF BIRTH",
        "DOB",
        "SIGNATURE",
        "NAME",
        "FATHER",
        "FATHER'S NAME"
    ]

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Remove OCR special characters
        clean_line = re.sub(r"[^A-Za-z ]", "", line)
        clean_line = re.sub(r"\s+", " ", clean_line).strip()

        if not clean_line:
            continue

        # Skip known labels
        if clean_line.upper() in skip_words:
            continue

        # Skip DOB
        if re.fullmatch(r"\d{2}[-/]\d{2}[-/]\d{4}", line):
            continue

        # Skip DL number
        if re.fullmatch(
                r"[A-Z]{2}[- ]?[0-9]{2}[- ]?[0-9]{4,11}",
                line.upper()
        ):
            continue

        # Possible name
        words = clean_line.split()

        if (
                len(words) >= 2
                and all(word.isalpha() for word in words)
                and all(len(word) >= 2 for word in words)
        ):
            name = clean_line
            break

    return {
        "document_type": "dl",
        "name": name,
        "dob": dob,
        "dl_number": dl_number
    }
if __name__ == "__main__":

    sample_text = """
    GOVERNMENT OF INDIA

    DRIVING LICENCE

    SAMARTH SHARMA

    DOB
    20-06-1986

    AP-0120190012345
    """

    result = extract_dl(sample_text)

    print(result)