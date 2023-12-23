import os, json, sys, glob
from pdf2image import convert_from_path

class PDFProcessor:
    def __init__(self, fileload: dict, output_dir: str) -> None:
        self.filename = f"{fileload['filename']}.{fileload['extension']}"
        self.output_dir = output_dir
        
        

    def to_image(self) -> None:
        """
        Converts a PDF to images and saves them in the output directory.
        """
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        pdfImages = convert_from_path(self.filename,dpi=500, fmt='jpeg',thread_count=9, poppler_path=r"C:\Program Files\poppler-23.11.0\Library\bin")
        return f"Successfully converted PDF to images"
    

    def orientation_check(self, single_image):
        '''Checks if the image is landscape or portrait.'''
        size = single_image.size
        if size[0] > size[1]:
            return "landscape"
        else:
            return "portrait"

    def image_orientation_check_and_adjust(self, imageObject):
        '''
        Checks the orientation of the image if landscape or portrait and adjusts it accordingly.
        Assumes that landscape images are double pages and portrait images are single pages.
        '''
        

    def page_split(self, single_image):
        '''
        Checks if the image is a double page and splits it into two images.
        '''
        orientation = self.orientation_check(single_image)
        if orientation == "landscape":
            width, height = single_image.size
            half_width = width/2
            left_side = single_image.crop((0, 0, half_width, height))
            right_side = single_image.crop((half_width, 0, width, height))
            return left_side, right_side
        else:
            return single_image
        
    def double_split():
        pass

        