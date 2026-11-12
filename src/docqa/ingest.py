import fitz
from pathlib import Path
import pymupdf

def load_pdf(file_path:str)->str:
    pdf_path = Path(file_path)
    #checking if the file path exists
    if (not pdf_path.exists()):raise FileNotFoundError(f"PDF not found: {file_path}")
    #checking the extension .pdf
    if ( pdf_path.suffix.lower()!=".pdf"):raise ValueError("The provided file is not a PDF.")

    extracted_text = []
    # we use with so when we exit from the with block, the document is automatically closed
    with pymupdf.open(pdf_path) as document:
        for page in document:
            page_text = page.get_text()
            extracted_text.append(page_text)
    return "\n".join(extracted_text)

print(load_pdf("data/raw/AI-CS-Detailed-Technical-Workshop-Report-2020.pdf"))

