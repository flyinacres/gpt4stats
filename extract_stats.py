import os
import json
import logging
import re
import fitz  # PyMuPDF for PDF text extraction
import argparse

def setup_logging():
    """
    Sets up logging to record diagnostic information.
    Logs are written to a file in the 'logs' directory.
    """
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        filename="logs/extract_stats.log",
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a given PDF file.
    Uses PyMuPDF (fitz) to read and extract text from each page.
    Logs a warning if no text is found.
    """
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text("text") for page in doc])
        if not text.strip():
            logging.warning("No text extracted from the PDF: %s", pdf_path)
        return text
    except Exception as e:
        logging.error("Error extracting text from PDF %s: %s", pdf_path, str(e))
        return ""

def clean_text(text):
    """
    Cleans extracted text by removing unwanted artifacts.
    - Normalizes spaces
    - Reduces excessive blank lines while preserving structure
    """
    if not isinstance(text, str):
        raise ValueError("Expected a string for text cleaning but got a non-string type.")
    text = re.sub(r'[^\S\r\n]+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'\n{2,}', '\n', text)  # Reduce multiple newlines to a single newline
    text = text.strip()
    return text

def segment_text_by_sections(text):
    """
    Segments text into sections based on common research paper headings.
    Returns a dictionary mapping section names to their content.
    Logs a warning if no sections are detected.
    """
    section_patterns = [r'(?i)\b(Abstract|Introduction|Methods?|Results?|Discussion|Conclusion)\b']
    sections = {}
    current_section = None
    for line in text.split("\n"):
        match = re.match(section_patterns[0], line.strip())
        if match:
            current_section = match.group(1)
            sections[current_section] = ""
        elif current_section:
            sections[current_section] += line + " "
    if not sections:
        logging.warning("No section headers found in extracted text.")
    return sections

def extract_p_values(text):
    """
    Extracts p-values using regular expressions.
    Identifies patterns such as 'p = 0.05' or 'p < 0.01'.
    """
    p_values = re.findall(r'\bp\s?[=<>]\s?0\.\d+\b', text)
    return {"p_values": p_values} if p_values else {}

def extract_confidence_intervals(text):
    """
    Extracts confidence intervals from text using regex.
    Identifies formats such as '95% CI [1.2, 2.3]'.
    """
    ci_matches = re.findall(r'\b\d{2,3}% CI \[[-+]?[0-9]*\.?[0-9]+, [-+]?[0-9]*\.?[0-9]+\]', text)
    return {"confidence_intervals": ci_matches} if ci_matches else {}

def extract_sample_sizes(text):
    """
    Extracts sample sizes from text using regex.
    Recognizes patterns like 'N = 100'.
    """
    sample_sizes = re.findall(r'\bN\s?=\s?\d+\b', text)
    return {"sample_sizes": sample_sizes} if sample_sizes else {}

def extract_statistical_data(text):
    """
    Runs all statistical extraction functions and combines results.
    """
    extracted_data = {}
    extracted_data.update(extract_p_values(text))
    extracted_data.update(extract_confidence_intervals(text))
    extracted_data.update(extract_sample_sizes(text))
    return extracted_data

def save_json_output(output_data, output_path):
    """
    Saves extracted data into a structured JSON file.
    """
    try:
        with open(output_path, "w", encoding="utf-8") as json_file:
            json.dump(output_data, json_file, indent=4)
        logging.info("Successfully saved JSON output to %s", output_path)
    except Exception as e:
        logging.error("Failed to save JSON output: %s", str(e))

def main():
    """
    Orchestrates the entire extraction process.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_path", help="Path to the PDF file to extract statistics from")
    args = parser.parse_args()

    pdf_path = args.pdf_path
    if not os.path.exists(pdf_path):
        logging.error("File not found: %s", pdf_path)
        return

    text = extract_text_from_pdf(pdf_path)
    if not text:
        logging.error("No text extracted, exiting.")
        return

    cleaned_text = clean_text(text)
    sections = segment_text_by_sections(cleaned_text)
    extracted_data = {section: extract_statistical_data(content) for section, content in sections.items()}

    output_path = os.path.splitext(pdf_path)[0] + ".json"
    save_json_output(extracted_data, output_path)

if __name__ == "__main__":
    setup_logging()
    main()

