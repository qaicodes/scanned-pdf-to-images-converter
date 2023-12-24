import os, json, sys, glob
from pdf2image import convert_from_path
import time
from utils.image_utils import ImageUtilities
import numpy as np
import pandas as pd



class PDFProcessor:
    
    def __init__(self, fileload: dict, output_dir: str) -> None:
        self.filename = f"{fileload['filename']}.{fileload['extension']}"
        self.output_dir = output_dir
        

    def _ticktick(func):
        def wrapper(self):
            start_time = time.time()
            func(self)
            print("--- %s seconds ---" % (time.time() - start_time))
        return wrapper
    
    @_ticktick
    def to_image(self) -> None:
        """
        Converts a PDF to images and saves them in the output directory.
        """
        page_index = 1
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        pdfImages = convert_from_path(self.filename,dpi=500, fmt='jpeg',thread_count=5, poppler_path=r"C:\Program Files\poppler-23.11.0\Library\bin")
        for image in pdfImages:
            print(f"Saving page {page_index}...")
            page_index += 1
            imgUtils = ImageUtilities(image)
            orientation = imgUtils.orientation_check(image)
            if orientation == "landscape":
                even_page_index = page_index + 1
                imgUtils.double_split(image, page_index, even_page_index, self.output_dir)
            else:
                image.save(f"{self.output_dir}/{page_index}.jpg")
        return f"Successfully converted PDF to images"
    
    



    

        