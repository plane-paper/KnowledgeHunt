import PyPDF2
import pdfplumber
from PyPDF2 import PdfWriter, PdfReader

def find_word_in_pdf(pdf_path, word):
    # Initialize a PDF reader
    pdf_reader = PdfReader(pdf_path)
    matching_pages = []
    
    # Iterate through each page
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text and word.lower() in text.lower():
                matching_pages.append(page_number)

    return matching_pages

def extract_pages_to_new_pdf(pdf_path, matching_pages, output_pdf_path):
    # Initialize a PDF reader and writer
    pdf_reader = PdfReader(pdf_path)
    pdf_writer = PdfWriter()
    
    # Add the matching pages to the writer
    for page_num in matching_pages:
        pdf_writer.add_page(pdf_reader.pages[page_num])
    
    # Write the new PDF to a file
    with open(output_pdf_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

def main():
    input_pdf = "Mathematics_analysis_and_approaches_paper_1__TZ1_HL.pdf"  # Path to your input PDF
    word_to_find = "sin"  # Word you're searching for
    output_pdf = "output.pdf"  # Path to save the new PDF

    # Find pages containing the word
    matching_pages = find_word_in_pdf(input_pdf, word_to_find)
    
    if matching_pages:
        # Extract matching pages to a new PDF
        extract_pages_to_new_pdf(input_pdf, matching_pages, output_pdf)
        print(f"Pages containing '{word_to_find}' have been saved to '{output_pdf}'.")
    else:
        print(f"No pages found containing the word '{word_to_find}'.")

if __name__ == "__main__":
    main()
