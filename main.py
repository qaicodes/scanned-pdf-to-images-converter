from pdf_utils.pdf_processor import PDFProcessor
import time




fileload = {
    "filename": "Book1",
    "extension": "pdf"
}

pdf = PDFProcessor(fileload, f"{fileload['filename']}_images")

if __name__ == "__main__":
    start_time = time.time()
    pdf.to_image()
    print("--- %s seconds ---" % (time.time() - start_time))
    # pdf.image_orientation_check()