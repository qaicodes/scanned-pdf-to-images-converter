from utils.pdf_processor import PDFProcessor
import time


fileload = {
    "filename": "A4-booklet-landscape",
    "extension": "pdf"
}

pdf = PDFProcessor(fileload, f"{fileload['filename']}_images")


if __name__ == "__main__":
    pdf.to_image()
    # pdf.image_orientation_check()