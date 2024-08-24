import PyPDF2
import re

def extract_references(pdf_path, output_file):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        # Extract text from all pages
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        # Find the references section
        references_match = re.search(r'References([\s\S]*)', text, re.IGNORECASE)
        if references_match:
            references = references_match.group(1)
            
            # Clean up the references
            references = re.sub(r'\n+', ' ', references)  # Remove multiple newlines
            references = re.sub(r'\s+', ' ', references)  # Remove extra whitespace
            
            # Split references into individual entries
            reference_list = re.split(r'\[\d+\]', references)
            
            # Write references to output file
            with open(output_file, 'w', encoding='utf-8') as out_file:
                for i, ref in enumerate(reference_list[1:], start=1):  # Skip the first empty split
                    if ref.strip():
                        out_file.write(f"[{i}] {ref.strip()}\n")  # Add numbering and single newline
            
            print(f"References extracted and saved to {output_file}")
        else:
            print("References section not found in the PDF.")

# Usage

pdf_path = 'path/to/your/paper.pdf'
output_file = 'references.txt'
extract_references(pdf_path, output_file)

