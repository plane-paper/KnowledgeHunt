import pdfplumber
import spacy
from PyPDF2 import PdfReader, PdfWriter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_nlp_model():
    try:
        return spacy.load("en_core_web_sm")
    except Exception as e:
        print("Error loading NLP model:", e)
        return None

def compute_tfidf_similarity(keywords, text):
    # Create a document from the keywords
    doc_keywords = " ".join(keywords)
    documents = [doc_keywords, text]
    vectorizer = TfidfVectorizer().fit_transform(documents)
    vectors = vectorizer.toarray()
    return cosine_similarity([vectors[0]], [vectors[1]])[0][0]

def filter_relevant_pages(input_pdf, keywords, output_pdf):
    nlp = load_nlp_model()
    if not nlp:
        print("NLP model not loaded. Exiting...")
        return ["ERROR", "NLP model not loaded"]

    pdf_reader = PdfReader(input_pdf)
    pdf_writer = PdfWriter()

    with pdfplumber.open(input_pdf) as pdf:
        for page_number, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue

            doc = nlp(text)
            
            # Use spaCy similarity if the model has vectors;
            # otherwise, fall back to TF-IDF based cosine similarity.
            if doc.has_vector:
                keyword_docs = [nlp(keyword) for keyword in keywords]
                similarity_score = sum(doc.similarity(kw_doc) for kw_doc in keyword_docs) / len(keyword_docs)
            else:
                similarity_score = compute_tfidf_similarity(keywords, text)
            
            # Named Entity Recognition check: count matching entities
            entities = [ent.text.lower() for ent in doc.ents]
            entity_match_count = sum(1 for keyword in keywords if any(keyword.lower() in ent for ent in entities))
            
            print(f"Page {page_number}: similarity_score = {similarity_score:.2f}, entity_match_count = {entity_match_count}")
            
            # Decide if page is relevant.
            # Thresholds: similarity > 0.3 (adjust as needed) or at least one matching entity.
            if similarity_score > 0.1 or entity_match_count > 0:
                pdf_writer.add_page(pdf_reader.pages[page_number])
    
    with open(output_pdf, "wb") as output:
        pdf_writer.write(output)
    return ["SUCCESS", None]