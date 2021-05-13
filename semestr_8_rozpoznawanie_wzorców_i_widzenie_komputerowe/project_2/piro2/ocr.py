import cv2
import numpy as np
import matplotlib.pyplot as plt

from .ocr_model import get_trained_model

class OCR:
    def __init__(self, debug=False):
        self.debug = debug
        self.window_width = 28
        self.window_height = 28
        self.step = 1
        self.model = get_trained_model()
    
    def scan(self, img):
        img = self.preprocess(img)

        slices = np.array([window.reshape((1, 28, 28)) for window in self.slide_window(img)])
        results = self.model.predict(slices)
        entropy = -(results * np.log10(results)).sum(axis=1)
        entropy_minima = np.r_[False, entropy[1:] < entropy[:-1]] & np.r_[entropy[:-1] < entropy[1:], False]

        slice_len = len(results)//6
        index = ''
        for i in range(6):
            sliced_res = results[i*slice_len:(i+1)*slice_len]
            sliced_entropy = entropy[i*slice_len:(i+1)*slice_len]
            entropied_sliced_res = sliced_res * (1 - sliced_entropy).reshape(sliced_entropy.shape[0],1).repeat(10, axis=1)
            agg_e_s_r = entropied_sliced_res.sum(axis=0)
            index += str(np.argmax(agg_e_s_r))

        #digits = results[entropy_minima, :].argmax(axis=1)
        #index = ''.join(map(str, digits))
        if self.debug:
            print(index)
            self.overview_plot(index, img, results, (1-entropy)*np.array(list(map(np.max,results))))
        return (None, None, index)
    
    def preprocess(self, img):
        img = 1 - img / 255
        mean = np.mean(img)
        std = np.std(img)
        norm = (np.tanh((img - mean) / std) + 1) / 2
        return norm * (norm > 0.5)
    
    def slide_window(self, img):
        img = self.resize_image(img)
        width = img.shape[1]
        result = []
        for x in range(0, width - self.window_width, self.step):
            columns = slice(x, x + self.window_width)
            yield img[:, columns]
    
    def overview_plot(self, title, img, results, entropy):
        plt.gray()
        plt.subplot(3, 1, 1)
        plt.title(title)
        plt.imshow(img)
        plt.subplot(3, 1, 2)
        plt.plot(results)
        plt.legend(np.arange(10))
        plt.subplot(3, 1, 3)
        plt.plot(entropy)
        plt.ylim(0, 1)
        plt.show()
    
    def window_plot(self, img, result):
        plt.gray()
        plt.subplot(2, 1, 1)
        plt.imshow(img)
        plt.subplot(2, 1, 2)
        plt.bar(list(range(10)), result)
        plt.show()

    def scan_digit(self, window):
        tensor = window.reshape((1, 1, 28, 28))
        result, = self.model.predict(tensor)
        digit = result.argmax()
        confidence = result[digit]
        self.window_plot(window, result)
        return digit, confidence

    def resize_image(self, img, zoom=1.2):
        height, width = img.shape
        crop_height = int(height / zoom)
        margin = (height - crop_height) // 2
        crop_y = slice(margin, height - margin)
        crop_x = slice(margin, width - margin)

        cropped = img[crop_y, crop_x]

        scale = min(1, self.window_height / cropped.shape[0])
        return cv2.resize(cropped, (0, 0), fx=scale, fy=scale)
