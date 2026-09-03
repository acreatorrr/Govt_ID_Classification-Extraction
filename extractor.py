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

    # Clean OCR lines
    clean_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Remove special characters
        cleaned = re.sub(r"[^A-Za-z ]", "", line)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        if cleaned:
            clean_lines.append(cleaned)

    # Words that should never be considered a name
    skip_words = {
        "GOVERNMENT OF INDIA",
        "GOVT OF INDIA",
        "GOVT. OF INDIA",
        "MY AADHAAR",
        "MALE",
        "FEMALE",
        "AADHAAR",
        "INDIA",
        "DOB",
        "DATE OF BIRTH",
        "MOBILE NO",
        "VID",
        "ISSUE DATE"
    }

    # Find DOB line
    dob_index = -1

    for i, line in enumerate(lines):
        if re.search(r"\d{2}[-/]\d{2}[-/]\d{4}", line):
            dob_index = i
            break

    # Look for a name before DOB
    if dob_index != -1:

        for i in range(dob_index - 1, -1, -1):

            line = lines[i].strip()

            if not line:
                continue

            # Remove OCR garbage
            candidate = re.sub(r"[^A-Za-z ]", "", line)
            candidate = re.sub(r"\s+", " ", candidate).strip()

            if not candidate:
                continue

            # Skip known text
            if candidate.upper() in skip_words:
                continue

            words = candidate.split()

            # Name should have at least two words
            if (
                    len(words) >= 2
                    and all(word.isalpha() for word in words)
                    and all(len(word) >= 2 for word in words)
            ):
                name = candidate
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

    for i, line in enumerate(lines):

        line = line.strip()

        if not line:
            continue

        # Look for "Name" label
        if re.search(r"\bName\b", line, re.IGNORECASE):

            # Check the next few lines
            for next_line in lines[i + 1:i + 4]:

                candidate = next_line.strip()

                if not candidate:
                    continue

                # Remove OCR special characters
                candidate = re.sub(r"[^A-Za-z ]", "", candidate)
                candidate = re.sub(r"\s+", " ", candidate).strip()

                if not candidate:
                    continue

                # Don't accept Father's Name
                if "FATHER" in candidate.upper():
                    continue

                # Don't accept common PAN labels
                skip_words = [
                    "INCOME TAX DEPARTMENT",
                    "GOVT OF INDIA",
                    "GOVT. OF INDIA",
                    "GOVERNMENT OF INDIA",
                    "PERMANENT ACCOUNT NUMBER",
                    "PERMANENT ACCOUNT NUMBER CARD",
                    "DATE OF BIRTH",
                    "SIGNATURE",
                    "FATHER NAME",
                    "FATHERS NAME"
                ]

                if candidate.upper() in skip_words:
                    continue

                # Don't accept PAN number
                if re.fullmatch(
                        r"[A-Z]{5}[0-9]{4}[A-Z]",
                        candidate.upper()
                ):
                    continue

                words = candidate.split()

                if (
                        len(words) >= 2
                        and all(word.isalpha() for word in words)
                        and all(len(word) >= 2 for word in words)
                ):
                    name = candidate
                    break

            if name != "unknown":
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
        "FATHER'S NAME",
        "BLOOD GROUP",
        "VALIDITY"
    ]

    # ---------------------------------
    # First: look for explicit Name label
    # ---------------------------------

    for i, line in enumerate(lines):

        line = line.strip()

        if not line:
            continue

        if re.search(r"\bName\b", line, re.IGNORECASE):

            for next_line in lines[i + 1:i + 4]:

                candidate = next_line.strip()

                if not candidate:
                    continue

                candidate = re.sub(r"[^A-Za-z ]", "", candidate)
                candidate = re.sub(r"\s+", " ", candidate).strip()

                if not candidate:
                    continue

                if candidate.upper() in skip_words:
                    continue

                words = candidate.split()

                if (
                        len(words) >= 2
                        and all(word.isalpha() for word in words)
                        and all(len(word) >= 2 for word in words)
                ):
                    name = candidate
                    break

            if name != "unknown":
                break

    # ---------------------------------
    # Second: fallback if Name not found
    # ---------------------------------

    if name == "unknown":

        for line in lines:

            line = line.strip()

            if not line:
                continue

            # Remove OCR garbage
            candidate = re.sub(r"[^A-Za-z ]", "", line)
            candidate = re.sub(r"\s+", " ", candidate).strip()

            if not candidate:
                continue

            if candidate.upper() in skip_words:
                continue

            # Skip DOB
            if re.search(r"\d{2}[-/]\d{2}[-/]\d{4}", line):
                continue

            # Skip DL number
            if re.fullmatch(
                    r"[A-Z]{2}[- ]?[0-9]{2}[- ]?[0-9]{4,11}",
                    candidate.upper()
            ):
                continue

            words = candidate.split()

            if (
                    len(words) >= 2
                    and all(word.isalpha() for word in words)
                    and all(len(word) >= 2 for word in words)
            ):
                name = candidate
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