from tkinter import *
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger
import os

# Function to select PDFs
def select_pdfs():
    files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])  
    if files:
        for file in files:
            pdf_listbox.insert(END, file)  # Show selected PDFs in the listbox

# Function to remove selected PDFs from the list
def remove_selected():
    selected_items = pdf_listbox.curselection()
    for index in reversed(selected_items):  
        pdf_listbox.delete(index)  # Remove selected PDF

# Function to merge selected PDFs
def merge_pdfs():
    files = pdf_listbox.get(0, END)  # Get all selected PDFs
    if not files:
        messagebox.showerror("Error", "No PDFs selected!")
        return

    output_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
        title="Save Merged PDF As"
    )

    if not output_path:
        return  # User canceled the save dialog

    try:
        merger = PdfMerger()
        for pdf in files:
            merger.append(pdf)

        merger.write(output_path)
        merger.close()

        messagebox.showinfo("Success", f"PDFs Merged Successfully!\nSaved as: {output_path}")
        os.startfile(os.path.dirname(output_path))

    except Exception as e:
        messagebox.showerror("Error", f"Failed to merge PDFs: {e}")

# Creating the merge window
merge_window = Tk()
merge_window.geometry("500x400")
merge_window.title("Merge PDFs")

Label(merge_window, text="Select PDFs to Merge", font=("Arial", 14, "bold")).pack(pady=10)

# Listbox to display selected PDFs
pdf_listbox = Listbox(merge_window, width=50, height=10)
pdf_listbox.pack(pady=10)

# Buttons to select and remove PDFs
Button(merge_window, text="Add PDFs", command=select_pdfs, font=("Arial", 12), bg="#007bff", fg="white").pack(pady=5)
Button(merge_window, text="Remove Selected", command=remove_selected, font=("Arial", 12), bg="#dc3545", fg="white").pack(pady=5)

# Merge button
Button(merge_window, text="Merge PDFs", command=merge_pdfs, font=("Arial", 12, "bold"), bg="#28a745", fg="white").pack(pady=10)

merge_window.mainloop()
