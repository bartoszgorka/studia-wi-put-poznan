import cv2
import numpy as np
import skimage.measure

from .worddetector import detect_words
from .ocr import OCR

class AttendanceList:
    def __init__(self, filename, debug=False):
        self.filename = filename
        self.debug = debug
        self.img = cv2.imread(self.filename, 0)
        self.ocr = OCR(debug)
    
    def entries(self):
        words = detect_words(self.filename)
        for row in np.unique(words)[1:]:
            mask = self.rightmost_block(words == row)
            yield self.ocr.scan(self.img[mask])
    
    def rightmost_block(self, mask):
        margin = 15
        regions = skimage.measure.label(mask * 1)
        props = skimage.measure.regionprops(regions)
        rightmost = max(props, key=lambda r: r.centroid[1])
        y, x = rightmost._slice
        x = slice(max(x.start - margin, 0), min(x.stop + margin, self.img.shape[1]))
        return y, x

