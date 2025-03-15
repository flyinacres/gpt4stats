import argparse
import json
import logging
import fitz
import re
import os

# Configure logging
logging.basicConfig(filename='logs/extraction.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text("text") for page in doc])
        return text
    except Exception as e:
        logging.error(f"Error extracting text: {e}")
        return ""


def clean_text(text):
    # Normalize spaces and remove excessive blank lines, but keep necessary newlines
    text = re.sub(r'[^\S\r\n]+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'\n{2,}', '\n', text)  # Reduce multiple newlines to a single newline
    text = text.strip()
    return text


def segment_sections(text):
    section_header_pattern = re.compile(
        r'^\s*(?:[IVX]+[.)]?)?\s*(METHODS|RESULTS|DISCUSSION|CONCLUSION)\s*$',
        re.IGNORECASE | re.MULTILINE
    )

    sections = {}
    current_section = None
    buffer = []

    for line in text.split("\n"):
        match = section_header_pattern.match(line)
        print(f"Match found: {match}")
        if match:
            if current_section:
                sections[current_section] = "\n".join(buffer).strip()
                print(f"Stored section: {current_section} (Length: {len(sections[current_section])})")  # Debug output

            current_section = match.group(1).upper()
            buffer = []
        else:
            buffer.append(line)

    if current_section:
        sections[current_section] = "\n".join(buffer).strip()
        print(f"Stored section: {current_section} (Length: {len(sections[current_section])})")  # Debug output

    return sections


def segment_text(text):
    """Segment text based on section headings."""
    sections = {}
    matches = re.finditer(r'(?m)^(METHODS|RESULTS|DISCUSSION|CONCLUSION)\b', text)
    positions = [(m.start(), m.group()) for m in matches]
    
    for i, (pos, title) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else None
        sections[title] = text[pos:end].strip()
    
    return sections

def extract_statistics(text):
    """Extract p-values, confidence intervals, sample sizes, and effect sizes."""
    stats = {
        "p_values": re.findall(r'p\s*[<>=]\s*0\.\d+', text, re.IGNORECASE),
        "confidence_intervals": re.findall(r'\d+% CI \[.*?\]', text),
        "sample_sizes": re.findall(r'N\s*=\s*\d+', text, re.IGNORECASE),
        "effect_sizes": re.findall(r'(Cohen\'s d|η²|r)\s*=\s*[-+]?[0-9]*\.?[0-9]+', text, re.IGNORECASE)
    }
    return stats

def save_to_json(output_path, data):
    """Save extracted statistics to a JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def main():
    parser = argparse.ArgumentParser(description='Extract statistical information from a research paper PDF.')
    parser.add_argument('pdf_path', help='Path to the input PDF file')
    args = parser.parse_args()
    
    if not os.path.exists(args.pdf_path):
        logging.error("File not found.")
        print("Error: File not found.")
        return
    
    logging.info(f"Processing file: {args.pdf_path}")
    text = extract_text_from_pdf(args.pdf_path)
    cleaned_text = clean_text(text)

    print(f"Extracted Text After Cleaning:\n{cleaned_text[:1000]}")  # Print the first 1000 characters



    #sections = segment_text(cleaned_text)
    sections = segment_sections(cleaned_text)
    print(f"Detected sections: {list(sections.keys())}")

    extracted_stats = {section: extract_statistics(content) for section, content in sections.items()}
    
    json_path = os.path.splitext(args.pdf_path)[0] + ".json"
    save_to_json(json_path, extracted_stats)
    
    print(f"Extraction complete. Results saved to {json_path}")
    logging.info(f"Extraction complete. JSON saved to {json_path}")

if __name__ == "__main__":
    main()

