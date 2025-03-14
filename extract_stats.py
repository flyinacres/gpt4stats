import argparse

def main():
    parser = argparse.ArgumentParser(description='Extract statistics from a research paper PDF.')
    parser.add_argument('pdf_path', type=str, help='Path to the PDF file')
    args = parser.parse_args()
    print(f'Processing file: {args.pdf_path}')

if __name__ == '__main__':
    main()