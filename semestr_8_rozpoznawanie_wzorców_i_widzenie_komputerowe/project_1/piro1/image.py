import math

import cv2
import numpy as np

from . import params


class Image:
    def __init__(self, filename):
        img = cv2.imread(filename, 0)
        self.img = self.rotate_with_scale(img)
        self.contour = cv2.findContours(self.img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1][0]
        self.polygon = cv2.approxPolyDP(self.contour, params.POLYGON_APPROX_EPSILON, closed=True)
        self.white_bars = self.calculate_white_bars()

    @staticmethod
    def rotate_with_scale(img):
        _, contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        rect = cv2.minAreaRect(max(contours, key=cv2.contourArea))
        with_border = img
        with_border = cv2.copyMakeBorder(with_border, 10, 10, 10, 10, cv2.BORDER_CONSTANT)
        angle = rect[2]
        if rect[1][0] < rect[1][1]:
            angle += 90.0

        height, width = min(with_border.shape), max(with_border.shape)
        rotation_mat = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1.0)
        rotated_image = cv2.warpAffine(with_border, rotation_mat, (int(width), int(height)))

        # Verify the cutting edge is up
        # Again find contours and rectangle
        _, contours, _ = cv2.findContours(rotated_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        rect2 = cv2.minAreaRect(max(contours, key=cv2.contourArea))
        cw, ch = rect2[0]
        w = max(rect2[1][0], rect2[1][1])
        h = min(rect2[1][0], rect2[1][1])

        # Move to (0, 0)
        move_matrix = np.float32([[1, 0, -(cw - w / 2)], [0, 1, -(ch - h / 2)]])
        moved_image = cv2.warpAffine(rotated_image, move_matrix, (int(w), int(h)))

        moments = cv2.moments(255 - moved_image)
        cx = int(moments['m10'] / moments['m00'])
        cy = int(moments['m01'] / moments['m00'])
        imbalance = cx / moved_image.shape[1] - 0.5
        if abs(imbalance) > params.HORIZONTAL_IMBALANCE_THRESHOLD:
            width, height = moved_image.shape
            rotation_mat = cv2.getRotationMatrix2D((width / 2, height / 2), math.copysign(90, imbalance), 1.0)
            moved_image = cv2.warpAffine(moved_image, rotation_mat, (int(width), int(height)))

        # Resize image
        image = cv2.resize(moved_image, (params.IMAGE_WIDTH, params.IMAGE_HEIGHT))

        # Count not zero (white) pixels
        white_pixels_on_top = np.count_nonzero(image[params.PIXELS_UP_DOWN_CALC, 0:params.IMAGE_WIDTH])
        white_pixels_on_bottom = np.count_nonzero(
            image[params.IMAGE_HEIGHT - params.PIXELS_UP_DOWN_CALC, 0:params.IMAGE_WIDTH])

        if white_pixels_on_top > white_pixels_on_bottom:
            # We need reverse image
            rotation_mat = cv2.getRotationMatrix2D((int(params.IMAGE_WIDTH / 2), int(params.IMAGE_HEIGHT / 2)),
                                                   params.IMAGE_HEIGHT - params.PIXELS_UP_DOWN_CALC, 1.0)
            image = cv2.warpAffine(image, rotation_mat, (params.IMAGE_WIDTH, params.IMAGE_HEIGHT))

        # Return rotated, reversed and scaled image
        return image

    def calculate_white_bars(self):
        vector = np.empty(shape=params.IMAGE_WIDTH, dtype=np.uint16)

        for i in range(0, params.IMAGE_WIDTH):
            vector[i] = np.count_nonzero(self.img[0:params.IMAGE_HEIGHT, i])
        return vector
