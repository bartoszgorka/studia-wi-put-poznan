#!/usr/bin/env python

import sys

from ocr import ocr

n = sys.argv[1] if len(sys.argv) > 1 else 1
filename = 'data/img_{}.jpg'.format(n)

for (name, surname, index) in ocr(filename, debug=True):
    print(index)
