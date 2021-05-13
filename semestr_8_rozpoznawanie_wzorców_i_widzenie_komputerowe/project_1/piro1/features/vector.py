import numpy as np

from .. import params


def match(image1, image2):
    vector_of_bars = np.add(image1.white_bars, image2.white_bars[::-1])
    variance = np.var(vector_of_bars, ddof=1)

    return params.IMAGE_WIDTH / variance
