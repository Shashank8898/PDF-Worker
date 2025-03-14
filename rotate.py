from tkinter import *
from tkinter import filedialog, messagebox
import PyPDF2
import os
import re

def select_pdf():
    """Opens a file dialog to select a PDF."""
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])  
    if file_path:
        file_entry.delete(0, END)
        file_entry.insert(0, file_path)

def parse_page_numbers(page_input, total_pages):
    """Parses the user-inputted page numbers and returns a list of valid page indices."""
    selected_pages = set()
    ranges = re.findall(r'\d+-\d+|\d+', page_input)  # Match single numbers or ranges

    for r in ranges:
        if "-" in r:  # Handle range (e.g., 2-5)
            start, end = map(int, r.split("-"))
            if 1 <= start <= end <= total_pages:
                selected_pages.update(range(start, end + 1))
        else:  # Handle single page (e.g., 3)
            page_num = int(r)
            if 1 <= page_num <= total_pages:
                selected_pages.add(page_num)

    return sorted(selected_pages)

def rotate_pdf(output_path=None):
    """Rotates only the selected pages in a PDF and saves the output file."""
    file_path = file_entry.get()
    page_input = page_entry.get().strip()
    rotation_angle = angle_var.get()

    if not file_path:
        messagebox.showerror("Error", "Please select a PDF file")
        return

    try:
        with open(file_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            writer = PyPDF2.PdfWriter()

            total_pages = len(reader.pages)
            selected_pages = parse_page_numbers(page_input, total_pages)

            if not selected_pages:
                messagebox.showerror("Error", "No valid pages selected")
                return

            for page_num in range(total_pages):
                page = reader.pages[page_num]
                if (page_num + 1) in selected_pages:  # Convert 1-based index to 0-based
                    page.rotate(rotation_angle)
                writer.add_page(page)

            # If no output path provided, ask for a new file
            if output_path is None:
                output_path = filedialog.asksaveasfilename(
                    defaultextension=".pdf",
                    filetypes=[("PDF Files", "*.pdf")],
                    title="Save Rotated PDF As"
                )
                if not output_path:
                    return  # User canceled the save dialog

            with open(output_path, "wb") as output_file:
                writer.write(output_file)

        messagebox.showinfo("Success", f"Rotated Pages: {selected_pages}\nSaved as: {output_path}")
        os.startfile(os.path.dirname(output_path))  # Open folder

    except Exception as e:
        messagebox.showerror("Error", f"Failed to rotate PDF: {e}")

def save_to_original():
    """Overwrites the original file after user confirmation."""
    file_path = file_entry.get()
    
    if not file_path:
        messagebox.showerror("Error", "Please select a PDF file")
        return
    
    confirm = messagebox.askyesno("Confirm Overwrite", f"Are you sure you want to overwrite {file_path}? This action cannot be undone.")
    
    if confirm:
        rotate_pdf(file_path)  # Overwrite the original file

# Create Rotate PDF Window
rotate_window = Tk()
rotate_window.geometry("450x400")
rotate_window.title("Rotate Specific PDF Pages")

Label(rotate_window, text="Select PDF to Rotate").pack(pady=5)
file_entry = Entry(rotate_window, width=50)
file_entry.pack(pady=5)
Button(rotate_window, text="Browse PDF", command=select_pdf).pack(pady=5)

Label(rotate_window, text="Enter Pages to Rotate (e.g., 1,3,5-7)").pack(pady=5)
page_entry = Entry(rotate_window, width=50)
page_entry.pack(pady=5)

Label(rotate_window, text="Select Rotation Angle").pack(pady=5)
angle_var = IntVar(value=90)
angle_dropdown = OptionMenu(rotate_window, angle_var, 90, 180, 270)
angle_dropdown.pack(pady=5)

# Buttons for saving
Button(rotate_window, text="Save As New PDF", command=rotate_pdf, bg="lightblue").pack(pady=5)
Button(rotate_window, text="Save to Original File", command=save_to_original, bg="red", fg="white").pack(pady=5)

# Run the rotate window
rotate_window.mainloop()
