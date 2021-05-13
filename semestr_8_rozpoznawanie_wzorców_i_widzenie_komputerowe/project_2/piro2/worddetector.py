import cv2
import numpy as np

def detect_words(filename):
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    words = np.zeros(img.shape[0:2])

    roi = region_of_interest(img)

    ink = np.full(img.shape[0:2], 255, dtype=np.uint8)
    ink[roi] = img[roi]

    ink = 255 - ink
    ink = cv2.adaptiveThreshold(ink, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY, 11, -15)

    sobeled = cv2.Sobel(img, cv2.CV_8U, 1, 0, ksize=3)
    sobeled = cv2.Sobel(sobeled, cv2.CV_8U, 0, 1, ksize=3)
    blurred = cv2.medianBlur(sobeled, 3)
    bilaterated = cv2.bilateralFilter(blurred,9,75,75)
    dilated = cv2.dilate(bilaterated, np.ones((5, 25)))
    closed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, np.ones((9, 23)))
    opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, np.ones((11, 11)))

    mask = np.array(opened>40, dtype=np.uint8)*255

    im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = [c for c in contours if cv2.contourArea(c)>1500]
    boundaries = divide_contours(contours)
    group_contours(boundaries, words)

    return words

MIN_Y = 0
MAX_Y = 1
MIN_X = 2
MAX_X = 3
AVG_Y = 4

def divide_contours(contours):
    boundaries = contour_boundaries(contours)
    heights = boundaries[:, MAX_X] - boundaries[:, MIN_X]
    mid_height = np.median(heights)
    rel_heights = heights / mid_height
    new_boundaries = []
    for i in range(boundaries.shape[0]):
        divided = [boundaries[i]]
        if rel_heights[i] > 3.3:
            divided = divide_boundary(boundaries[i], 3)
        elif rel_heights[i] > 2:
            divided = divide_boundary(boundaries[i], 2)
        new_boundaries.extend(divided)
    return np.array(new_boundaries)

def divide_boundary(boundary, num_slices):
    min_y, max_y, min_x, max_x = boundary
    slice_height = int((max_x - min_x) / num_slices)
    slices = []
    x = min_x
    for i in range(num_slices):
        slices.append([min_y, max_y, x, x + slice_height])
        x += slice_height
    return slices

def contour_boundaries(contours):
    boundaries = np.zeros((len(contours), 4), dtype=int)
    for i, contour in enumerate(contours):
        boundaries[i, MIN_Y] = contour[:, :, 0].min()
        boundaries[i, MAX_Y] = contour[:, :, 0].max()
        boundaries[i, MIN_X] = contour[:, :, 1].min()
        boundaries[i, MAX_X] = contour[:, :, 1].max()
    return boundaries

def group_contours(boundaries, words):
    avg_y = (boundaries[:, MAX_X] + boundaries[:, MIN_X]) / 2
    indices = np.argsort(avg_y)
    row = 0
    last_avg_y = 0
    for i in indices:
        min_y, max_y, min_x, max_x = boundaries[i, :]
        if avg_y[i] - last_avg_y > 20:
            row += 1

        words[min_x:max_x, min_y:max_y] = row
        last_avg_y = avg_y[i]

def region_of_interest(img):
    # Cast to gray scale
    gray = np.float32(img)
    mask = np.full(gray.shape, False)

    # Edge detect
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)
    y, x = np.where(dst > 0.01 * dst.max())

    min_x, min_y = min(x), min(y)
    max_x, max_y = max(x), max(y)

    mask[int(min_y):int(max_y), int(min_x):int(max_x)] = True
    return mask
