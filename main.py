from utils.pdf_processor import PDFProcessor
import time


fileload = {
    "filename": "Book1",
    "extension": "pdf"
}

pdf = PDFProcessor(fileload, f"{fileload['filename']}_images")


if __name__ == "__main__":
    pdf.organise_pdf_file()
    # pdf.image_orientation_check()