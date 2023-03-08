import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger

# Initialize tkinter
root = tk.Tk()

# Set window size and title
root.geometry("800x480")
root.title("SPARKMINDA PDF MERGER APP")

# Load logo from assets folder
logo_path = os.path.join("assets", "SparkmindaLogo.png")
logo_image = tk.PhotoImage(file=logo_path)

# Create label for app title
app_title_label = tk.Label(root, text="SPARKMINDA PDF MERGER APP", height=0, font=("Verdana", 20, "bold"))


# Create frame 1 for Browse button and selected folder label
frame1 = tk.Frame(root, height=100, bd=2, relief="solid", bg="white")


# Create Browse button and folder path label
def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_path_label.config(text=folder_path)


browse_button = tk.Button(frame1, text="Browse", command=browse_folder)
folder_path_label = tk.Label(frame1, text="", bg="white")

# Position Browse button and folder path label
browse_button.pack(side="left", padx=5, pady=10)
folder_path_label.pack(side="left", padx=5, pady=10)

# Create frame 2 for Select PDF files button and selected files list
frame2 = tk.Frame(root, height=100, bd=2, relief="solid", bg="white")

# Create Select PDF files button and selected files listbox
selected_files_listbox = tk.Listbox(frame2)


def select_files():
    files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    for file in files:
        selected_files_listbox.insert(tk.END, file)


select_files_button = tk.Button(frame2, text="Select PDF files", command=select_files)

# Position Select PDF files button and selected files listbox
select_files_button.pack(side="left", padx=5, pady=10)
selected_files_listbox.pack(side="left", padx=5, pady=10, fill="both", expand=True)


#import os
#import PyPDF2

def repair_pdf_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            filepath = os.path.join(directory, filename)
            try:
                pdf = PyPDF2.PdfFileReader(open(filepath, "rb"), strict=False)
                pdf.getNumPages()  # Force PyPDF2 to read the PDF file and detect any errors
            except PyPDF2.utils.PdfReadError:
                # If there is an error while reading the PDF, try repairing it
                writer = PyPDF2.PdfFileWriter()
                reader = PyPDF2.PdfFileReader(open(filepath, "rb"), strict=False)
                for page in range(reader.getNumPages()):
                    writer.addPage(reader.getPage(page))
                with open(filepath, "wb") as output_file:
                    writer.write(output_file)

# Create Merge PDF button


def merge_files():
    merger = PdfMerger()
    for file in selected_files_listbox.get(0, tk.END):
        merger.append(file)
    output_folder = "output_folder"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_file_path = os.path.join(output_folder, filedialog.asksaveasfilename(defaultextension=".pdf",
                                                                                filetypes=[("PDF files", "*.pdf")]))
    merger.write(output_file_path)
    merger.close()
    messagebox.showinfo("Success", "PDF Merged Successfully")


merge_button = tk.Button(root, text="Merge PDF", command=merge_files)
# Position logo, app title, frames, and Merge PDF button
logo_label = tk.Label(root, image=logo_image)
logo_label.pack(side="top", anchor="ne", padx=5, pady=5)
app_title_label.pack(side="top", anchor="nw", padx=0, pady=0)
frame1.pack(side="top", fill="x", padx=10, pady=10)
frame2.pack(side="top", fill="both", padx=10, pady=10, expand=True)
merge_button.pack(side="top", pady=10)

# Start the tkinter event loop
root.mainloop()
