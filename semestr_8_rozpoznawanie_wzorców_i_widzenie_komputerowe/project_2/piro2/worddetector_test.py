import glob
import os.path
import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np

COLORS = np.array([
    (51, 102, 204), (220, 57, 18), (255, 153, 0), (16, 150, 24), (153, 0, 153),
    (59, 62, 172), (0, 153, 198), (221, 68, 119), (102, 170, 0), (184, 46, 46),
    (49, 99, 149), (153, 68, 153), (34, 170, 153), (170, 170, 17), (102, 51, 204),
    (230, 115, 0), (139, 7, 7), (50, 146, 98), (85, 116, 166), (59, 62, 172)
])
ESCAPE_KEY = 27

def mark_words(img, words, opacity=0.3):
    overlay = np.copy(img)
    for num in np.unique(words)[1:]:
        mask = words == num
        color_index = (int(num) - 1) % len(COLORS)
        color = COLORS[color_index]
        overlay[mask] = color
    return cv2.addWeighted(img, 1 - opacity, overlay, opacity, 0)

def resize_to_fit(img, max_height=800):
    height = img.shape[0]
    scale = min(1, max_height / height)
    return cv2.resize(img, (0, 0), fx=scale, fy=scale)

def display_image(img, title=""):
    if len(img.shape) == 3:
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        plt.gray()
        rgb_img = img
    plt.title(title)
    plt.imshow(rgb_img)
    plt.show()

if __name__ == '__main__':
    from .worddetector import detect_words
    
    if len(sys.argv) > 1:
        filenames = sys.argv[1:]
    else:
        pattern = os.path.join(os.path.dirname(__file__), '..', 'data', '*.jpg')
        filenames = glob.glob(pattern)
    
    for filename in filenames:
        words = detect_words(filename)
        img = cv2.imread(filename)
        assert(words.shape == (img.shape[0], img.shape[1]))
        img_overlay = mark_words(img, words)
        img_resized = resize_to_fit(img_overlay)
        try:
            display_image(img_resized, os.path.basename(filename))
        except KeyboardInterrupt:
            break
