#!/usr/bin/env python

import sys

from base64 import b64decode
from zlib import decompress
from PIL import Image


def main():
    # Read in each individual coin line, and combine it
    cl_1 = read_fileline('data/coin_line_1')
    cl_2 = read_fileline('data/coin_line_2')
    cl_3 = read_fileline('data/coin_line_3')
    cl_4 = read_fileline('data/coin_line_4')
    combined_coin = ''.join([cl_1, cl_2, cl_3, cl_4])

    print "Combined Coin Data:\n%s" % combined_coin

    # Assuming the coin data is base64 encoded, lets decode it
    b64data = b64decode(combined_coin)

    # Lets attempt to decompress this with zlib
    print "Attempting to decompress data..."
    decompressed_data = decompress(b64data)
    print "Data decompressed with zlib into monochome binary image data"

    # Binary data appears to be a monochrome image, let's create a bmp with PIL
    # and output it
    image_array = []
    black = (0, 0, 0)
    white = (255, 255, 255)
    img_size = 42  # Image is a square, so we only need 1 value
    clean_data = ''.join(
        [format(ord(y), '#010b')[2:] for y in decompressed_data]
    )
    for x in clean_data[:-4]:
        if x == '1':
            image_array.append(black)
        elif x == '0':
            image_array.append(white)
        # An else here would catch new lines, we can just ignore them

    # Create an image using PIL with our image_array
    print "Creating 42x42 bmp QR code image from data..."
    img = Image.new("RGB", (img_size, img_size), "white")

    # Replace the pixels with our image_array data
    pixels = img.load()
    idx = 0
    for i in range(0, img_size):
        for j in range(0, img_size):
            pixels[i, j] = image_array[idx]
            idx += 1

    # Let's save our new image as a bitmap
    img.save('solution.bmp')

    print "Done"
    sys.exit(0)


def read_fileline(path):
    with open(path, 'rb') as f:
        return f.read().strip()


if __name__ == "__main__":
    main()
