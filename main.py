import pdfplumber
import re
from PyPDF2 import PdfReader, PdfWriter

# Extract text from PDF and track pages
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        pages_text = {}
        for i, page in enumerate(pdf.pages):
            pages_text[i] = page.extract_text()
    return pages_text

# Extract questions from pages
def extract_questions(pages_text):
    questions = {}
    question_pattern = r"(\d+\. .*?\?)"  # Pattern for questions (adjust as needed)

    for page_num, page_text in pages_text.items():
        page_questions = re.findall(question_pattern, page_text, re.DOTALL)
        for question in page_questions:
            if question not in questions:
                questions[question] = []
            questions[question].append(page_num)
    
    return questions

# Categorize questions based on keywords
def categorize_by_content(questions, categories):
    categorized_questions = {category: [] for category in categories}
    
    # Check for category keywords in each question
    for question, pages in questions.items():
        for category, keywords in categories.items():
            if any(keyword.lower() in question.lower() for keyword in keywords):
                categorized_questions[category].append((question, pages))
    
    return categorized_questions

# Select relevant pages based on category
def select_relevant_pages(categorized_questions, selected_category):
    selected_pages = set()
    for question, pages in categorized_questions[selected_category]:
        selected_pages.update(pages)
    return sorted(list(selected_pages))  # Return pages in order

# Create a new PDF with relevant pages
def create_contiguous_pdf(input_pdf, output_pdf, selected_pages):
    pdf_reader = PdfReader(input_pdf)
    pdf_writer = PdfWriter()

    for page_num in selected_pages:
        pdf_writer.add_page(pdf_reader.pages[page_num])

    with open(output_pdf, "wb") as output_file:
        pdf_writer.write(output_file)

# Main execution
def main():
    pdf_path = "path_to_your_exam.pdf"  # Path to the PDF file
    output_pdf = "output_exam.pdf"  # Output PDF file
    categories = {
        "Functions": ["function", "graph", "domain", "range", "f(x)", "g(x)", "h(x)"],
        "Integrals": ["integral", "area", "definite integral", "indefinite integral", "integration", "∫"],
        "Derivatives": ["derivative", "rate of change", "d/dx", "slope", "tangent"],
        "Limits": ["limit", "approaches", "∞", "tends to"],
        "Trigonometry": ["sine", "cosine", "tan", "sec", "csc", "trig", "angle", "radians"],
    }
    
    # Step 1: Extract text from PDF
    pages_text = extract_text_from_pdf(pdf_path)
    
    # Step 2: Extract questions
    questions = extract_questions(pages_text)
    
    # Step 3: Categorize questions by content
    categorized_questions = categorize_by_content(questions, categories)
    
    # Step 4: Select relevant pages (example: category "Integrals")
    selected_category = "Integrals"  # Change this based on the category you want
    selected_pages = select_relevant_pages(categorized_questions, selected_category)
    
    # Step 5: Create a new PDF with the selected pages
    create_contiguous_pdf(pdf_path, output_pdf, selected_pages)

if __name__ == "__main__":
    main()
