import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter


def extract_text_from_pdf(file_path):
    """
    Extracts text from each page of a PDF file using pdfplumber.
    """
    text_pages = []
    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                text_pages.append((text, page_number))
    return text_pages


def chunk_text_by_page(text_pages, chunk_size=2500):
    """
    Splits text from each page into chunks.
    """
    all_chunks = []
    for text, page_number in text_pages:
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size)
        chunks = splitter.split_text(text)
        all_chunks.extend((chunk, page_number) for chunk in chunks)
    return all_chunks
