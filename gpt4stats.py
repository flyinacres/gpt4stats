import os
import sys
import argparse
import subprocess

# Define project structure
def setup_project():
    directories = ["tests", "logs"]
    files = {
        "requirements.txt": "pymupdf\nregex",
        "extract_stats.py": """
import argparse

def main():
    parser = argparse.ArgumentParser(description='Extract statistics from a research paper PDF.')
    parser.add_argument('pdf_path', type=str, help='Path to the PDF file')
    args = parser.parse_args()
    print(f'Processing file: {args.pdf_path}')

if __name__ == '__main__':
    main()
        """.strip()
    }
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    for file, content in files.items():
        with open(file, "w") as f:
            f.write(content)

    print("Project structure created successfully.")

# Create virtual environment and install dependencies
def setup_virtual_env():
    subprocess.run([sys.executable, "-m", "venv", "venv"])
    subprocess.run(["venv/bin/pip", "install", "-r", "requirements.txt"] if os.name != 'nt' else ["venv\\Scripts\\pip", "install", "-r", "requirements.txt"])
    print("Virtual environment set up and dependencies installed.")

if __name__ == "__main__":
    setup_project()
    setup_virtual_env()

