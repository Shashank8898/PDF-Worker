from tkinter import *
from tkinter import filedialog, messagebox
from pdf2docx import Converter

def select_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        file_entry.delete(0, END)
        file_entry.insert(0, file_path)

def convert_to_word():
    pdf_path = file_entry.get()
    if not pdf_path:
        messagebox.showerror("Error", "Please select a PDF file")
        return
    
    # Ask user for save location
    docx_path = filedialog.asksaveasfilename(
        defaultextension=".docx",
        filetypes=[("Word Files", "*.docx")],
        title="Save Word File As"
    )

    if not docx_path:
        return  # User canceled save dialog

    try:
        converter = Converter(pdf_path)
        converter.convert(docx_path, start=0, end=None)
        converter.close()

        messagebox.showinfo("Success", f"PDF converted to Word!\nSaved at: {docx_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert PDF: {e}")

# Create tkinter window
root = Tk()
root.geometry("600x200")
root.title("PDF to Word Converter")

Label(root, text="Select PDF to Convert").pack(pady=10)

file_entry = Entry(root, width=50)
file_entry.pack()

Button(root, text="Browse PDF", command=select_pdf).pack(pady=5)
Button(root, text="Convert to Word", command=convert_to_word, bg="green", fg="white").pack(pady=10)

root.mainloop()
