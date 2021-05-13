def match(img1, img2):
    count1 = img1.polygon.shape[0]
    count2 = img2.polygon.shape[0]

    return 1 - abs(count1 - count2) / (0.5 * (count1 + count2))
