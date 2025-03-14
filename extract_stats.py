import argparse
import fitz

def extract_text_from_pdf(pdf_path):
    try:
        with fitz.open(pdf_path) as doc:
            text = " ".join([page.get_text() for page in doc])
        return text
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Extract statistics from a research paper PDF.')
    parser.add_argument('pdf_path', type=str, help='Path to the PDF file')
    args = parser.parse_args()
    
    text = extract_text_from_pdf(args.pdf_path)
    if text:
        print(text)

if __name__ == '__main__':
    main()
