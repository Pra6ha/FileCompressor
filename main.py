import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import pytesseract
import subprocess
from datetime import datetime
from core import compress_pdf_to_pdfa, generate_output_pdf  # Importing core functions for PDF handling

# Set the path for Tesseract OCR executable (update this if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\office\Desktop\Doc\tesseract.exe'


# Function to convert image to a searchable PDF with OCR (from the 3rd code)
def convert_image_to_pdf_with_ocr(input_image_path, output_pdf_path):
    try:
        # Open the image using Pillow
        img = Image.open(input_image_path)

        # Convert image to RGB (necessary for PNG images with alpha channel)
        img = img.convert('RGB')

        # Use Tesseract to extract text from the image
        extracted_text = pytesseract.image_to_string(img)
        print("OCR Text extracted: ", extracted_text)

        # Save the image as a PDF with OCR text (this will create a searchable PDF)
        img.save(output_pdf_path, "PDF", resolution=100.0)
        print(f"Image with OCR text saved to PDF: {output_pdf_path}")

    except Exception as e:
        print(f"Error converting image to searchable PDF: {e}")
        return


# Function to convert an image to a searchable PDF/A by performing OCR and then converting to PDF/A
def convert_image_to_pdfa_with_ocr(input_image_path, output_pdfa_path):
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Step 1: Convert the image to a searchable PDF (with OCR)
    pdf_output_path = "temp_output_with_ocr.pdf"  # Temporary PDF path
    convert_image_to_pdf_with_ocr(input_image_path, pdf_output_path)

    if not os.path.exists(pdf_output_path):
        print("Error: PDF conversion failed.")
        return

    # Step 2: Convert the generated PDF to PDF/A
    compress_pdf_to_pdfa(pdf_output_path, output_pdfa_path)

    # Clean up temporary PDF file
    if os.path.exists(pdf_output_path):
        os.remove(pdf_output_path)
        print("Temporary PDF file cleaned up.")


# Function to handle the file upload and decide which conversion to apply
def submit_form():
    name = name_entry.get()
    file_path = file_label.cget("text")

    if not name or file_path == "No file selected":
        messagebox.showwarning("Input Error", "Please fill in all fields and select a file.")
    else:
        # Get file extension to determine file type
        file_extension = os.path.splitext(file_path)[1].lower()
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_pdfa_path = fr'C:\Users\office\Desktop\tessOCR\{name}_{current_datetime}.pdf'

        # If it's an image (JPG, PNG, JPEG), run the image-to-PDF/A with OCR
        if file_extension in ['.jpg', '.jpeg', '.png']:
            convert_image_to_pdfa_with_ocr(file_path, output_pdfa_path)
            messagebox.showinfo("Success", f"Image converted to PDF/A with OCR: {output_pdfa_path}")

        # If it's a PDF, run the compress PDF to PDF/A (core.py logic)
        elif file_extension == '.pdf':
            output_pdf = generate_output_pdf(name)
            success = compress_pdf_to_pdfa(file_path, output_pdf)
            if success:
                messagebox.showinfo("Success", f"PDF converted to PDF/A: {output_pdf}")
            else:
                messagebox.showerror("Error", "Failed to convert the PDF.")

        # If the file type is unsupported
        else:
            messagebox.showerror("Unsupported File", "Please upload a valid image (JPG, PNG, JPEG) or PDF file.")


# Function to handle file upload
def upload_file():
    file_path = filedialog.askopenfilename(title="Select a file",
                                           filetypes=[("PDF Files", "*.pdf"), ("Image Files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        file_label.config(text=file_path)
    else:
        file_label.config(text="No file selected")


# Function to clear all inputs
def clear_form():
    name_entry.delete(0, tk.END)  # Clear the name entry
    file_label.config(text="No file selected")  # Reset file label


# Function to close the application
def close_app():
    root.quit()  # Close the Tkinter window


# Create the main window
root = tk.Tk()
root.title("PDF Upload and Conversion")

# Create the name label and entry field
name_label = tk.Label(root, text="Enter Your Name:")
name_label.grid(row=0, column=0, padx=10, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=5)

# Create the file upload button and label
upload_button = tk.Button(root, text="Upload File", command=upload_file)
upload_button.grid(row=1, column=0, padx=10, pady=5)
file_label = tk.Label(root, text="No file selected", width=40, anchor="w")
file_label.grid(row=1, column=1, padx=10, pady=5)

# Create the submit button
submit_button = tk.Button(root, text="Submit", command=submit_form)
submit_button.grid(row=2, column=0, padx=10, pady=20)

# Create the clear button
clear_button = tk.Button(root, text="Clear", command=clear_form)
clear_button.grid(row=2, column=1, padx=10, pady=20)

# Create the close button
close_button = tk.Button(root, text="Close", command=close_app)
close_button.grid(row=2, column=2, padx=10, pady=20)

# Run the application
root.mainloop()
