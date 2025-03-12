import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
from PIL import Image, ImageTk
import os

#Local imports
from ctrl_f_based import find_keywords_in_pdf
from ctrl_f_based import extract_pages_to_new_pdf
from nlp_based import filter_relevant_pages


def process_pdf(input_pdf, selected_type, output_pdf, status_label):
    keyword_dict = {
        "Functions": ["function", "functions", "tangent", "graph", "domain", "range", "f(x)", "g(x)", "h(x)","f(", "g(", "sketch", "intersection", "codomain", "composite", "inverse", "reflection", "translation", "dilation", "stretch", "compression", "shift", "symmetry", "polynomial", "rational", "exponential", "logarithm", "asymptote", "intercept", "inflection", "gradient"],
        "Integrals": ["integral", "area", "definite", "indefinite", "integration", "∫"],
        "Derivatives": ["derivative", "rate of change", "d/dx", "slope", "tangent"],
        "Limits": ["limit", "approaches", "∞", "tends to"],
        "Trigonometry": ["sin", "cos", "tan", "sec", "csc", "trig", "angle", "radians"],
    }
    
    keywords = keyword_dict.get(selected_type)
    if not keywords:
        messagebox.showerror("Error", "Invalid type selected.")
        return
    
    if not os.path.exists(input_pdf):
        messagebox.showerror("Error", "Invalid input PDF path.")
        return

    status_label.config(text=f"Searching for keywords in the '{selected_type}' category...")
    
    matching_pages = find_keywords_in_pdf(input_pdf, keywords)

    if matching_pages[0] == "ERROR":
        messagebox.showerror("Error", "There was an error processing the PDF: " + str(matching_pages[1]))
        status_label.config(text="Status: Waiting for input...") #Reset status label
        return 
    
    if matching_pages:
        #extract_pages_to_new_pdf(input_pdf, matching_pages, output_pdf)
        extract_pages_to_new_pdf(input_pdf, matching_pages, "temp.pdf")
        status_label.config(text=f"Pages containing '{selected_type}' have been preliminarily saved to 'temp.pdf'.")
        #status = filter_relevant_pages(output_pdf, keywords, output_pdf)
        status = filter_relevant_pages("temp.pdf", keywords, output_pdf)
        if status[0] == "ERROR":
            messagebox.showerror("Error", "There was an error processing the PDF: " + str(status[1]))
            status_label.config(text="Status: Waiting for input...")
            return
        else:
            status_label.config(text=f"SUCCESS!! Relevant pages saved to '{output_pdf}'.")
    else:
        status_label.config(text=f"FAILED!! No pages found containing keywords from the '{selected_type}' category.")

def on_process_pdf(input_pdf_entry, type_combobox, output_pdf_entry, status_label):
    input_pdf = input_pdf_entry.get()
    selected_type = type_combobox.get()
    output_pdf = output_pdf_entry.get()

    if not output_pdf:
        output_pdf = "output.pdf"

    if not input_pdf or selected_type == "Select Type":
        messagebox.showerror("Error", "Please fill in all fields and select a type.")
        return
    
    processing_thread = threading.Thread(target=process_pdf, args=(input_pdf, selected_type, output_pdf, status_label))
    processing_thread.start()


def create_ui():
    # Create main window
    root = tk.Tk()
    root.title("KnowledgeHunt")

    root.resizable(False, False)
    
    try:
        icon = Image.open("icon.ico")  # Replace with your icon file path
        icon = ImageTk.PhotoImage(icon)
        root.iconphoto(True, icon)
    except Exception as e:
        print(f"Error setting window icon: {e}")
    
    # Input PDF Label and Entry
    input_pdf_label = tk.Label(root, text="Input PDF Path:")
    input_pdf_label.grid(row=0, column=0, padx=10, pady=5)
    input_pdf_entry = tk.Entry(root, width=50)
    input_pdf_entry.grid(row=0, column=1, padx=10, pady=5)

    # Output PDF Label and Entry
    output_pdf_label = tk.Label(root, text="Output PDF Path\n(leave blank for output.pdf\nin current directory):")
    output_pdf_label.grid(row=1, column=0, padx=10, pady=5)
    output_pdf_entry = tk.Entry(root, width=50)
    output_pdf_entry.grid(row=1, column=1, padx=10, pady=5)

    # Type Selection Label and Combobox
    type_label = tk.Label(root, text="Select Type:")
    type_label.grid(row=2, column=0, padx=10, pady=5)
    type_combobox = ttk.Combobox(root, values=["Select Type", "Functions", "Integrals", "Derivatives", "Limits", "Trigonometry"], state="readonly")
    type_combobox.grid(row=2, column=1, padx=10, pady=5)
    type_combobox.set("Select Type")

    # Status Label
    status_label = tk.Label(root, text="Status: Waiting for input...", relief="sunken", width=60, height=2)
    status_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    # Process Button
    process_button = tk.Button(root, text="Process PDF", command=lambda: on_process_pdf(input_pdf_entry, type_combobox, output_pdf_entry, status_label))
    process_button.grid(row=3, column=0, columnspan=2, pady=20)

    # Run the GUI
    print("UI Created.")
    root.mainloop()