import fitz
from pathlib import Path
import pymupdf
import re


def clean_pdf(extracted_text:str)->str:
    cleaned_text = extracted_text.replace("\r\n","\n").replace("\r","\n")
    cleaned_text = cleaned_text.replace("\x00","")
    cleaned_text = re.sub(r"[ \t]+"," ",cleaned_text)
    cleaned_text = "\n".join( line.strip() for line in cleaned_text.split("\n"))
    cleaned_text = re.sub(r"\n{3,}", "\n\n", cleaned_text)
    cleaned_text = cleaned_text.strip()
    return cleaned_text



 
def load_pdf(file_path:str)->list[dict]:
    pdf_path = Path(file_path)
    #checking if the file path exists
    if (not pdf_path.exists()):raise FileNotFoundError(f"PDF not found: {file_path}")
    #checking the extension .pdf
    if ( pdf_path.suffix.lower()!=".pdf"):raise ValueError("The provided file is not a PDF.")

    pages = []
    # we use with so when we exit from the with block, the document is automatically closed
    with pymupdf.open(pdf_path) as document:
        for page_number,page in enumerate(document,start=1):
            page_text = page.get_text()
            if page_text:
                pages.append(
                    {
                        "text" : clean_pdf(page_text),
                        "page_number":page_number,
                         "source":pdf_path.name
                     }
                  )
    return pages

def chunck_pages(pages:list[dict],chunck_size:int,overlap:int)->list[dict]:
    if overlap>=chunck_size:raise ValueError("The overlap should be less than the chunck size.")
    chuncks = []
    for page in pages:
        page_text = page["text"]
        start = 0
        chunk_number = 0
        while start<len(page_text):
            end = start+chunck_size
            chunck_text = page_text[start:end].strip()
            if chunck_text:
                chuncks.append(
                    {"text":chunck_text,
                     "chunk_id":f"page_number: {page["page_number"]} / chunck number:{chunk_number}",
                     "source":page["source"],
                     "page": page["page_number"],
                     }
                    
                )
                start = end-overlap
                chunk_number+=1
            if end>=len(page_text):break
    return chuncks




if __name__ == "__main__":
    pages = load_pdf("data/raw/AI-CS-Detailed-Technical-Workshop-Report-2020.pdf")
    chunks = chunck_pages(pages, 800, 150)

    print(f"pages kept: {len(pages)}")
    print(f"chunks: {len(chunks)}")
    sizes = [len(c["text"]) for c in chunks]
    print(f"chunk size min/avg/max: {min(sizes)} / {sum(sizes) // len(sizes)} / {max(sizes)}")
    print(f"empty chunks: {sum(1 for s in sizes if s == 0)}")
    print(f"unique ids: {len({c['chunk_id'] for c in chunks}) == len(chunks)}")

    for c in (chunks[0], chunks[len(chunks) // 2], chunks[-1]):
        print("\n" + "-" * 60)
        print(c["chunk_id"], "| page", c["page"])
        print(c["text"])