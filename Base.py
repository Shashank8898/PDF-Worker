from tkinter import *
from tkinter import filedialog, messagebox
import subprocess
import PyPDF2
import os
import re




# Creating a tkinter window
root = Tk()
root.geometry("600x450")
root.title("PDF Worker")
root.configure(bg="#f0f0f0")  # Light gray background

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size to match screen size
root.geometry(f"{screen_width}x{screen_height}")

# Optionally maximize the window (Windows)
root.state("zoomed")

# Styling
btn_style = {
    "font": ("Arial", 12, "bold"),
    "fg": "white",
    "width": 20,
    "height": 2,
    "borderwidth": 2,
    "relief": "raised"
}

frame = Frame(root, bg="#ffffff", padx=20, pady=20)
frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

Label(frame, text="PDF Operations", font=("Arial", 16, "bold"), bg="#ffffff").pack(pady=10)

def open_search():
    subprocess.run(["python", "search.py"])

def open_converter():
    subprocess.run(["python", "convert.py"])

def open_rotate_window():
    subprocess.run(["python", "rotate.py"])
    


def open_merge_window():
    subprocess.run(["python", "merge_window.py"])

def open_compress_window():
    """Opens a new window for compressing PDFs."""
    compress_win = Toplevel(root)
    compress_win.geometry("400x250")
    compress_win.title("Compress PDF")
    compress_win.configure(bg="#ffffff")

    Label(compress_win, text="Compress PDF", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)

    file_entry = Entry(compress_win, width=40, font=("Arial", 10))
    file_entry.pack(pady=5)

    def select_pdf():
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            file_entry.delete(0, END)
            file_entry.insert(0, file_path)

    def compress_pdf():
        input_pdf = file_entry.get()
        if not input_pdf:
            messagebox.showerror("Error", "Please select a PDF file")
            return

        output_pdf = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Save Compressed PDF As"
        )

        if not output_pdf:
            return  # User canceled the save dialog

        result = subprocess.run(["python", "compress.py", input_pdf, output_pdf], capture_output=True, text=True)

        if result.returncode == 0:
            messagebox.showinfo("Success", f"PDF Compressed Successfully!\nSaved as: {output_pdf}")
        else:
            messagebox.showerror("Error", "Failed to compress PDF")

    Button(compress_win, text="Browse PDF", command=select_pdf, bg="#007bff", fg="white").pack(pady=5)
    Button(compress_win, text="Compress PDF", command=compress_pdf, bg="#28a745", fg="white").pack(pady=10)

def open_pdf_viewer():
    subprocess.run(["python", "pdf_viewer.py"])




# Buttons
Button(frame, text="Merge PDFs", command=open_merge_window, **btn_style, bg="#28a745").pack(pady=5)
Button(frame, text="Rotate pages", command=open_rotate_window, **btn_style, bg="#17a2b8").pack(pady=5)
Button(frame, text="Convert PDF to Word", command=open_converter, **btn_style, bg="#dc3545").pack(pady=5)
Button(frame, text="Search Text in PDF", command=open_search, **btn_style, bg="#6f42c1").pack(pady=5)
Button(frame, text="Compress PDF", command=open_compress_window, **btn_style, bg="#ffc107").pack(pady=5)
Button(root, text="View PDF", command=open_pdf_viewer, **btn_style, bg="#007bff").pack(pady=5)


root.mainloop()
