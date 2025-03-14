import argparse
import fitz
import re

def extract_text_from_pdf(pdf_path):
    try:
        with fitz.open(pdf_path) as doc:
            text = "\n".join([page.get_text() for page in doc])
        return text
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces and new lines
    text = text.encode('utf-8', 'ignore').decode('utf-8')  # Normalize encoding
    return text.strip()

def segment_text(text):
    sections = {}
    current_section = "INTRODUCTION"  # Default section
    sections[current_section] = ""
    
    for line in text.split("\n"):
        line = line.strip()
        if re.match(r'^(METHODS|RESULTS|DISCUSSION|CONCLUSION|REFERENCES)$', line, re.IGNORECASE):
            current_section = line.upper()
            sections[current_section] = ""
        else:
            sections[current_section] += line + " "
    
    return sections

def extract_p_values(text):
    p_value_pattern = r'p\s*[<>=]\s*\d*\.\d+'
    p_values = re.findall(p_value_pattern, text, re.IGNORECASE)
    return {"p_values": p_values}

def extract_statistics(text):
    ci_pattern = r'\d+% CI \[\s*-?\d+\.\d+,\s*-?\d+\.\d+\]'
    sample_size_pattern = r'N\s*=\s*\d+'
    effect_size_pattern = r'Cohen\'s d\s*=\s*-?\d+\.\d+'
    
    confidence_intervals = re.findall(ci_pattern, text)
    sample_sizes = re.findall(sample_size_pattern, text)
    effect_sizes = re.findall(effect_size_pattern, text)
    
    return {
        "confidence_intervals": confidence_intervals,
        "sample_sizes": sample_sizes,
        "effect_sizes": effect_sizes
    }

def main():
    parser = argparse.ArgumentParser(description='Extract statistics from a research paper PDF.')
    parser.add_argument('pdf_path', type=str, help='Path to the PDF file')
    args = parser.parse_args()
    
    text = extract_text_from_pdf(args.pdf_path)
    if text:
        cleaned_text = clean_text(text)
        sections = segment_text(cleaned_text)
        for section, content in sections.items():
            print(f"\n=== {section} ===\n{content}\n")
            print(f"Extracted p-values: {extract_p_values(content)}")
            print(f"Extracted statistics: {extract_statistics(content)}")

if __name__ == '__main__':
    main()
