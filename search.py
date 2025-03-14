from tkinter import *
from tkinter import filedialog, messagebox
from pdf2image import convert_from_path
from PIL import Image, ImageTk, ImageDraw
import pytesseract

# Configure Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"

def select_pdf():
    """Opens a file dialog to select a PDF file and displays it."""
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        file_entry.delete(0, END)
        file_entry.insert(0, file_path)
        display_pdf_images(file_path)

def display_pdf_images(pdf_path):
    """Converts PDF pages to images and displays them."""
    global images, displayed_images
    try:
        images = convert_from_path(pdf_path)
        displayed_images = images[:]
        update_image_display()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load PDF: {e}")

def highlight_text():
    """Highlights occurrences of the searched text in images."""
    global displayed_images
    query = search_entry.get().strip()
    if not query:
        messagebox.showerror("Error", "Enter a search term!")
        return

    highlighted_images = []
    
    for img in images:
        img_copy = img.copy()
        draw = ImageDraw.Draw(img_copy)
        text_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

        for i, word in enumerate(text_data["text"]):
            if query.lower() in word.lower():
                x, y, w, h = text_data["left"][i], text_data["top"][i], text_data["width"][i], text_data["height"][i]
                draw.rectangle([x, y, x + w, y + h], outline="red", width=3)

        highlighted_images.append(img_copy)

    displayed_images = highlighted_images
    update_image_display()

def update_image_display():
    """Updates the displayed images and resizes them to fit the window."""
    if not displayed_images:
        return
    
    img = displayed_images[0]  # Display first page only
    resize_and_show(img)

def resize_and_show(img):
    """Resizes the image to fit the window and displays it."""
    canvas_width = image_frame.winfo_width()
    canvas_height = image_frame.winfo_height()

    if canvas_width > 1 and canvas_height > 1:
        # Maintain aspect ratio
        img_ratio = img.width / img.height
        frame_ratio = canvas_width / canvas_height

        if img_ratio > frame_ratio:
            new_width = canvas_width
            new_height = int(new_width / img_ratio)
        else:
            new_height = canvas_height
            new_width = int(new_height * img_ratio)

        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(resized_img)

        canvas.delete("all")  # Clear previous images
        canvas.create_image(canvas_width // 2, canvas_height // 2, anchor=CENTER, image=img_tk)
        canvas.image = img_tk  # Prevent garbage collection

def on_resize(event):
    """Handles window resizing and updates the image."""
    if displayed_images:
        resize_and_show(displayed_images[0])

# Create Tkinter window
root = Tk()
root.geometry("900x700")
root.title("Search & Highlight Text in PDF")

# PDF Selection
Label(root, text="Select PDF").pack(pady=5)
file_entry = Entry(root, width=50)
file_entry.pack()
Button(root, text="Browse PDF", command=select_pdf).pack(pady=5)

# Search Functionality
Label(root, text="Enter text to search").pack(pady=5)
search_entry = Entry(root, width=30)
search_entry.pack()
Button(root, text="Search & Highlight", command=highlight_text, bg="purple", fg="white").pack(pady=10)

# Image Display Frame with Canvas
image_frame = Frame(root, bg="gray")
image_frame.pack(pady=10, fill=BOTH, expand=True)

canvas = Canvas(image_frame, bg="black")
canvas.pack(fill=BOTH, expand=True)

# Bind resize event
root.bind("<Configure>", on_resize)

root.mainloop()
