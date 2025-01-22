import PyPDF2
import pdfplumber
from PyPDF2 import PdfWriter, PdfReader

def find_keywords_in_pdf(pdf_path, keywords):
    # Initialize a PDF reader
    try:
        pdf_reader = PdfReader(pdf_path)
    except Exception as e:
        return ["ERROR", e]
    
    matching_pages = []
    
    # Iterate through each page
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text and any(keyword.lower() in text.lower() for keyword in keywords):
                    matching_pages.append(page_number)
    except Exception as e:
        return ["ERROR", e]


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


'''OBSOLETE CODE'''
# def main(): #This is for testing only
#     input_pdf = r"test.pdf"  # Path to your input PDF
#     output_pdf = "output.pdf"  # Path to save the new PDF

#     # Dictionary with types as keys and lists of keywords as values
#     keyword_dict = {
#         "Functions": ["function", "graph", "domain", "range", "f(x)", "g(x)", "h(x)"],
#         "Integrals": ["integral", "area", "definite integral", "indefinite integral", "integration", "∫"],
#         "Derivatives": ["derivative", "rate of change", "d/dx", "slope", "tangent"],
#         "Limits": ["limit", "approaches", "∞", "tends to"],
#         "Trigonometry": ["sin", "cos", "tan", "sec", "csc", "trig", "angle", "radians"],
#     }

#     # Prompt the user to choose a type
#     print("Choose a type to search for:")
#     for i, key in enumerate(keyword_dict.keys(), start=1):
#         print(f"{i}. {key}")

#     try:
#         choice = int(input("\nEnter the number of your choice: "))
#         selected_type = list(keyword_dict.keys())[choice - 1]
#         keywords = keyword_dict[selected_type]
#         print(f"Searching for keywords in the '{selected_type}' category...")

#         # Find pages containing any of the selected keywords
#         matching_pages = find_keywords_in_pdf(input_pdf, keywords)
        
#         if matching_pages:
#             # Extract matching pages to a new PDF
#             extract_pages_to_new_pdf(input_pdf, matching_pages, output_pdf)
#             print(f"Pages containing keywords from the '{selected_type}' category have been saved to '{output_pdf}'.")
#         else:
#             print(f"No pages found containing any of the keywords from the '{selected_type}' category.")
#     except (ValueError, IndexError):
#         print("Invalid choice. Please enter a valid number.")

# if __name__ == "__main__":
#     main()
