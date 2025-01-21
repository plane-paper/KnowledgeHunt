import spacy
import pdfplumber
from PyPDF2 import PdfReader, PdfWriter
import re  # Importing the regex module for question detection

# Load spaCy model for NLP processing
nlp = spacy.load("en_core_web_sm")

# Step 1: Extract text from the PDF and track pages
def extract_text_from_pdf(pdf_path):
    """Extract text from each page of the PDF."""
    print(f"Opening PDF file: {pdf_path}")
    with pdfplumber.open(pdf_path) as pdf:
        pages_text = {}
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:  # Only store pages with extracted text
                pages_text[i] = page_text
            else:
                print(f"Warning: No text extracted from page {i + 1}.")
    print(f"Extracted text from {len(pages_text)} pages.")
    # Debug: Print the first 500 characters of the extracted text for the first page (if exists)
    if pages_text:
        print(f"Preview of extracted text from page 1: {list(pages_text.values())[0][:500]}")
    return pages_text

# Step 2: Extract questions from text using regex
def extract_questions(pages_text):
    """Identify and extract questions from the text."""
    questions = {}

    for page_num, page_text in pages_text.items():
        print(f"Processing Page {page_num + 1} for questions...")
        
        # Preprocessing: Clean up unwanted symbols (e.g., bullets or unwanted characters)
        cleaned_text = page_text.replace("y", "").replace("\n", " ").strip()

        # Use regex to find sentences that end with a question mark
        page_questions = re.findall(r"([^.]*\?)", cleaned_text)  # Match any sentence ending with a ?

        if page_questions:
            print(f"Page {page_num + 1}: Found questions -> {page_questions}")
        
        for question in page_questions:
            if question not in questions:
                questions[question] = []
            questions[question].append(page_num)

    print(f"Total questions extracted: {len(questions)}")
    return questions

# Step 3: Categorize questions based on similarity to keywords
def categorize_by_content(questions, categories):
    """Categorize questions by similarity to predefined category keywords."""
    categorized_questions = {category: [] for category in categories}

    for question, pages in questions.items():
        doc = nlp(question)
        
        for category, keywords in categories.items():
            category_doc = nlp(" ".join(keywords))
            similarity = doc.similarity(category_doc)  # Measure similarity between question and category keywords
            
            # Debug: Show the similarity score
            print(f"Question: {question}")
            print(f"Category: {category} - Similarity Score: {similarity:.2f}")
            
            # Consider a question relevant to a category if the similarity exceeds a threshold
            if similarity > 0.3:  # You can adjust this threshold for better categorization
                categorized_questions[category].append((question, pages))
                print(f"Question categorized under {category}: {question}")
    
    # Debug: Print out how many questions belong to each category
    for category, questions_list in categorized_questions.items():
        print(f"Category: {category} - Questions: {len(questions_list)}")
    
    return categorized_questions

# Step 4: Select relevant pages based on the selected category
def select_relevant_pages(categorized_questions, selected_category):
    """Select pages that are relevant to the chosen category."""
    selected_pages = set()
    for question, pages in categorized_questions[selected_category]:
        selected_pages.update(pages)
    
    print(f"Selected {len(selected_pages)} pages for category {selected_category}.")
    return sorted(list(selected_pages))  # Return pages in sorted order

# Step 5: Create a new PDF with relevant pages
def create_contiguous_pdf(input_pdf, output_pdf, selected_pages):
    """Create a new PDF with the selected pages from the input PDF."""
    if not selected_pages:
        print("No pages selected.")
        return
    
    print(f"Creating new PDF with selected pages: {selected_pages}")
    pdf_reader = PdfReader(input_pdf)
    pdf_writer = PdfWriter()

    for page_num in selected_pages:
        try:
            pdf_writer.add_page(pdf_reader.pages[page_num])  # Add each selected page
        except IndexError:
            print(f"Error: Page number {page_num} is out of range.")
            continue

    with open(output_pdf, "wb") as output_file:
        pdf_writer.write(output_file)
    print(f"New PDF created with selected pages: {output_pdf}")

# Main execution
def main():
    pdf_path = r"Mathematics_analysis_and_approaches_paper_1__TZ1_HL.pdf"  # Path to the PDF file
    output_pdf = "output_exam.pdf"  # Output PDF file
    categories = {
        "Functions": ["function", "graph", "domain", "range", "f(x)", "g(x)", "h(x)"],
        "Integrals": ["integral", "area", "definite integral", "indefinite integral", "integration", "∫"],
        "Derivatives": ["derivative", "rate of change", "d/dx", "slope", "tangent"],
        "Limits": ["limit", "approaches", "∞", "tends to"],
        "Trigonometry": ["sine", "cosine", "tan", "sec", "csc", "trig", "angle", "radians"],
    }
    
    # Step 1: Extract text from the PDF
    pages_text = extract_text_from_pdf(pdf_path)
    
    # Step 2: Extract questions
    questions = extract_questions(pages_text)
    
    if not questions:
        print("No questions extracted.")
        return
    
    # Step 3: Categorize questions by content
    categorized_questions = categorize_by_content(questions, categories)
    
    if not any(categorized_questions.values()):
        print("No questions categorized.")
        return
    
    # Step 4: Select relevant pages for a selected category
    selected_category = "Functions"  # Change this based on the category you want
    selected_pages = select_relevant_pages(categorized_questions, selected_category)
    
    if not selected_pages:
        print(f"No relevant pages found for category {selected_category}.")
        return
    
    # Step 5: Create a new PDF with the selected pages
    create_contiguous_pdf(pdf_path, output_pdf, selected_pages)

if __name__ == "__main__":
    main()
