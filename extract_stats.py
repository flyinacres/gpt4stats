import argparse
import fitz
import re

def extract_text_from_pdf(pdf_path):
    try:
        with fitz.open(pdf_path) as doc:
            text = " ".join([page.get_text() for page in doc])
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

def main():
    parser = argparse.ArgumentParser(description='Extract statistics from a research paper PDF.')
    parser.add_argument('pdf_path', type=str, help='Path to the PDF file')
    args = parser.parse_args()
    
    text = extract_text_from_pdf(args.pdf_path)
    if text:
        cleaned_text = clean_text(text)
        print(cleaned_text)

if __name__ == '__main__':
    main()
