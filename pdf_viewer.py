from tkinter import *
from tkinter import filedialog
import fitz  # PyMuPDF
from PIL import Image, ImageTk
import webbrowser

class PDFViewer:
    def __init__(self, root):
        self.root = root
        self.root.geometry("900x700")
        self.root.title("PDF Viewer")
        self.root.configure(bg="#ffffff")

        Label(self.root, text="PDF Viewer", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)

        # Canvas for PDF display
        self.canvas = Canvas(self.root, bg="#ffffff", cursor="hand2")
        self.scrollbar_y = Scrollbar(self.root, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar_x = Scrollbar(self.root, orient=HORIZONTAL, command=self.canvas.xview)

        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.frame = Frame(self.canvas, bg="#ffffff")
        self.window_id = self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar_y.pack(side=RIGHT, fill=Y)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)

        # Zoom buttons
        btn_frame = Frame(self.root, bg="#ffffff")
        btn_frame.pack(pady=5)

        Button(btn_frame, text="Zoom In", command=self.zoom_in, bg="#28a745", fg="white", font=("Arial", 12, "bold")).pack(side=LEFT, padx=10)
        Button(btn_frame, text="Zoom Out", command=self.zoom_out, bg="#dc3545", fg="white", font=("Arial", 12, "bold")).pack(side=LEFT, padx=10)

        # Load PDF
        self.file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not self.file_path:
            self.root.destroy()
            return

        self.doc = fitz.open(self.file_path)
        self.zoom_factor = 1.0  # Default zoom
        self.images = []
        self.links = {}  # Store link positions
        self.render_pdf()

        # Bind mouse controls
        self.canvas.bind("<MouseWheel>", self.scroll_pdf)  # Scroll inside canvas
        self.root.bind("<Control-MouseWheel>", self.mouse_zoom)
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.check_link_click)  # Check for links

        self.start_x = 0
        self.start_y = 0

    def render_pdf(self):
        """Render the PDF pages with the current zoom factor."""
        for widget in self.frame.winfo_children():
            widget.destroy()  # Clear previous images

        self.images = []
        self.links = {}

        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            matrix = fitz.Matrix(self.zoom_factor, self.zoom_factor)  # Apply zoom
            pix = page.get_pixmap(matrix=matrix)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img_tk = ImageTk.PhotoImage(img)
            self.images.append(img_tk)

            # Label for each page
            label = Label(self.frame, image=img_tk, bg="#ffffff")
            label.pack(pady=5)

            # Store links for this page
            self.links[page_num] = []
            for link in page.get_links():
                if "uri" in link:
                    rect = link["from"]
                    self.links[page_num].append((rect, link["uri"]))

            # Enable scroll on the PDF itself
            label.bind("<MouseWheel>", self.scroll_pdf)
            label.bind("<ButtonPress-1>", self.start_drag)
            label.bind("<B1-Motion>", self.on_drag)
            label.bind("<ButtonRelease-1>", lambda e, p=page_num: self.check_link_click(e, p))

        self.frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoom_in(self):
        """Increase zoom factor and re-render PDF."""
        self.zoom_factor += 0.2
        self.render_pdf()

    def zoom_out(self):
        """Decrease zoom factor and re-render PDF."""
        if self.zoom_factor > 0.4:
            self.zoom_factor -= 0.2
            self.render_pdf()

    def mouse_zoom(self, event):
        """Zoom in or out using the mouse scroll while holding Ctrl."""
        if event.delta > 0:  # Scroll up
            self.zoom_in()
        else:  # Scroll down
            self.zoom_out()

    def scroll_pdf(self, event):
        """Scroll the PDF when hovering over it."""
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def start_drag(self, event):
        """Start tracking mouse movement for dragging."""
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        """Move the canvas view when dragging the mouse."""
        self.canvas.xview_scroll(self.start_x - event.x, "units")
        self.canvas.yview_scroll(self.start_y - event.y, "units")
        self.start_x = event.x
        self.start_y = event.y

    def check_link_click(self, event, page_num=0):
        """Check if a link was clicked and open it in a browser."""
        if page_num not in self.links:
            return

        # Convert event coordinates to PDF space
        x = event.x * (1 / self.zoom_factor)
        y = event.y * (1 / self.zoom_factor)

        for rect, uri in self.links[page_num]:
            x0, y0, x1, y1 = rect
            if x0 <= x <= x1 and y0 <= y <= y1:
                webbrowser.open(uri)
                return

if __name__ == "__main__":
    root = Tk()
    PDFViewer(root)
    root.mainloop()
