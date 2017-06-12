import numpy
from collections import Counter

import png


def otsu(histogram, total_pixels):
    mu_total = sum(g * histogram.get(g) for g in range(256))
    max_t = 0
    max_value = 0
    p1 = 0.0
    mu1 = 0.0
    for t in range(256 - 1):
        p1 += histogram.get(t)
        p2 = total_pixels - p1
        if p1 == 0 or p2 == 0:
            continue
        mu1 += histogram.get(t) * t
        mu2 = mu_total - mu1

        tmp = p1 * p2 * (mu1 / p1 - mu2 / p2) ** 2
        if tmp > max_value:
            max_value = tmp
            max_t = t
    return max_t


def apply_threshold(png_file, threshold):
    with open(png_file, 'r') as f:
        bitmap = png.Reader(f).asDirect()
        new_bitmap = []
        for row in bitmap[2]:
            shape = len(row)
            new_row = numpy.empty(shape)
            for i in range(shape):
                new_row[i] = 0 if row[i] <= threshold else 255
            new_bitmap.append(new_row)
    return new_bitmap


def binarize(png_file, output_file):
    with open(png_file, 'r') as f:
        reader = png.Reader(f)
        data = reader.asDirect()
        bitmap = data[2]
        counter = Counter()
        for row in bitmap:
            counter.update(row)
        total_pixels = data[0] * data[1]
        threshold = otsu(counter, total_pixels)
    new_bitmap = apply_threshold(png_file, threshold)
    with open(output_file, 'wb') as f:
        w = png.Writer(data[0], data[1], greyscale=True, bitdepth=8, gamma=1.0, background=(1,))
        w.write(f, new_bitmap)


binarize("../resources/graysample.png", "../resources/graysample2.png")
