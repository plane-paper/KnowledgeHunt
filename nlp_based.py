import spacy
import pdfplumber
from PyPDF2 import PdfReader, PdfWriter

# Load spaCy model for NLP processing
nlp = spacy.load("en_core_web_sm")

# Extract text from PDF and track pages
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        pages_text = {}
        for i, page in enumerate(pdf.pages):
            pages_text[i] = page.extract_text()
    return pages_text

# Extract questions from pages using NLP
def extract_questions(pages_text):
    questions = {}
    
    for page_num, page_text in pages_text.items():
        doc = nlp(page_text)
        page_questions = [sent.text for sent in doc.sents if "?" in sent.text]  # Extract sentences with question mark
        
        if page_questions:
            print(f"Page {page_num + 1}: Found questions -> {page_questions}")
        
        for question in page_questions:
            if question not in questions:
                questions[question] = []
            questions[question].append(page_num)
    
    return questions

# Categorize questions based on NLP similarity to category keywords
def categorize_by_content(questions, categories):
    categorized_questions = {category: [] for category in categories}
    
    # Process each question and categorize based on similarity to category keywords
    for question, pages in questions.items():
        doc = nlp(question)
        for category, keywords in categories.items():
            category_doc = nlp(" ".join(keywords))
            similarity = doc.similarity(category_doc)  # Measure similarity between question and category keywords
            
            # Adjust threshold if necessary (0.3 or lower to capture more questions)
            if similarity > 0.3:  # Reduced threshold for better matching
                categorized_questions[category].append((question, pages))
                print(f"Question categorized under {category}: {question}")
    
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
    pdf_path = r"C:\Users\Richard\Desktop\Mathematics_analysis_and_approaches_paper_1__TZ1_HL.pdf"  # Path to the PDF file
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
    
    # Check if any questions are extracted
    if not questions:
        print("No questions extracted.")
        return
    
    # Step 3: Categorize questions by content
    categorized_questions = categorize_by_content(questions, categories)
    
    # Check if any questions are categorized
    if not any(categorized_questions.values()):
        print("No questions categorized.")
        return
    
    # Step 4: Select relevant pages (example: category "Integrals")
    selected_category = "Functions"  # Change this based on the category you want
    selected_pages = select_relevant_pages(categorized_questions, selected_category)
    
    if not selected_pages:
        print(f"No relevant pages found for category {selected_category}.")
        return
    
    # Step 5: Create a new PDF with the selected pages
    create_contiguous_pdf(pdf_path, output_pdf, selected_pages)
    print(f"New PDF created with selected pages: {output_pdf}")

if __name__ == "__main__":
    main()
