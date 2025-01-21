import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading

#Local imports
from ctrl_f_based import find_keywords_in_pdf
from ctrl_f_based import extract_pages_to_new_pdf


def process_pdf(input_pdf, selected_type, output_pdf, status_label):
    keyword_dict = {
        "Functions": ["function", "graph", "domain", "range", "f(x)", "g(x)", "h(x)"],
        "Integrals": ["integral", "area", "definite integral", "indefinite integral", "integration", "∫"],
        "Derivatives": ["derivative", "rate of change", "d/dx", "slope", "tangent"],
        "Limits": ["limit", "approaches", "∞", "tends to"],
        "Trigonometry": ["sin", "cos", "tan", "sec", "csc", "trig", "angle", "radians"],
    }
    
    keywords = keyword_dict.get(selected_type)
    if not keywords:
        messagebox.showerror("Error", "Invalid type selected.")
        return
    
    status_label.config(text=f"Searching for keywords in the '{selected_type}' category...")
    matching_pages = find_keywords_in_pdf(input_pdf, keywords)
    
    if matching_pages:
        extract_pages_to_new_pdf(input_pdf, matching_pages, output_pdf)
        messagebox.showinfo("Success", f"Pages containing '{selected_type}' have been saved to '{output_pdf}'.")
    else:
        messagebox.showinfo("No Matches", f"No pages found containing keywords from the '{selected_type}' category.")

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
    root.title("PDF Keyword Extractor")

    # Input PDF Label and Entry
    input_pdf_label = tk.Label(root, text="Input PDF Path:")
    input_pdf_label.grid(row=0, column=0, padx=10, pady=5)
    input_pdf_entry = tk.Entry(root, width=50)
    input_pdf_entry.grid(row=0, column=1, padx=10, pady=5)

    # Output PDF Label and Entry
    output_pdf_label = tk.Label(root, text="Output PDF Path:")
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
    root.mainloop()