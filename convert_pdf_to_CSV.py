import PyPDF2
from pdf2image import convert_from_path
import easyocr
import re
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import datetime
import os
import numpy as np

# Function to select PDF file
def select_pdf_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    return file_path

# Function to create output directory
def create_output_directory(base_directory):
    now = datetime.datetime.now()
    dir_name = now.strftime("%Y%m%d_%H%M%S")
    output_directory = os.path.join(base_directory, dir_name)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    return output_directory

# Main function to process PDF and save text to CSV
def process_pdf_and_save_to_csv(pdf_path, poppler_path):
    if not pdf_path:
        print("No PDF file selected.")
        return

    base_directory = os.path.dirname(pdf_path)
    output_directory = create_output_directory(base_directory)
    reader = easyocr.Reader(['en'])

    all_lines = []

    # Convert PDF pages to images and perform OCR
    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    for page_num, image in enumerate(images):
        np_image = np.array(image)
        results = reader.readtext(np_image)
        for result in results:
            line_text = result[1]
            all_lines.append(line_text)
            print(f"OCR line from page {page_num + 1}: {line_text}")  # Debug output

    # Clean each line and prepare for CSV
    cleaned_lines = [re.sub(r'\s+', ' ', line).strip() for line in all_lines if line.strip()]

    # Save each cleaned line to a new row in CSV
    df = pd.DataFrame(cleaned_lines, columns=['Line'])
    csv_file_path = os.path.join(output_directory, 'ocr_text_dataset.csv')
    df.to_csv(csv_file_path, index=False)
    print(f"Text data saved as {csv_file_path}")

# Define Poppler path
poppler_path = 'bin'  # Update this path
pdf_path = select_pdf_file()
process_pdf_and_save_to_csv(pdf_path, poppler_path)
