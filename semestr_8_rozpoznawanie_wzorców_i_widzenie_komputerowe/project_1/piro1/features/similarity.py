from scipy import stats


def match(image1, image2):
    similarity = abs(stats.pearsonr(image1.white_bars, image2.white_bars)[0])
    reversed_similarity = abs(stats.pearsonr(image1.white_bars, image2.white_bars[::-1])[0])
    return max(similarity, reversed_similarity)
