import pdfplumber
import os

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts text from a PDF file."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"{pdf_path} not found.")
    
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            full_text += page.extract_text()
    
    # Check if PDF was scanned or if it contains text
    if not full_text.strip():
        raise ValueError("No text found in the PDF. The document may be scanned.")
    
    return full_text
