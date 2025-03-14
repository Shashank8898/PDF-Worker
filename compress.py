import sys
import fitz  # PyMuPDF

def compress_pdf(input_pdf, output_pdf):
    doc = fitz.open(input_pdf)
    doc.save(output_pdf, garbage=4, deflate=True, clean=True)

def function():
    print("Hello World")
    

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compress.py <input_pdf> <output_pdf>")
        sys.exit(1)

    input_pdf, output_pdf = sys.argv[1], sys.argv[2]

    try:
        compress_pdf(input_pdf, output_pdf)
        print("PDF compressed successfully!")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
