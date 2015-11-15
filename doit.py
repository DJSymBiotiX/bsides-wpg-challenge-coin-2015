#!/usr/bin/env python

from base64 import b64decode
from zlib import decompress


def main():
    # Read in the 2 hashes, don't know if we need them though
    program_hash = read_fileline('data/program_data')
    badge_hash = read_fileline('data/badge_data')

    print "Program Hash: %s" % program_hash
    print "  Badge Hash: %s" % badge_hash

    # Read in each individual coin line, and combine it
    cl_1 = read_fileline('data/coin_line_1')
    cl_2 = read_fileline('data/coin_line_2')
    cl_3 = read_fileline('data/coin_line_3')
    cl_4 = read_fileline('data/coin_line_4')
    combined_coin = ''.join([cl_1, cl_2, cl_3, cl_4])

    print "Combined Coin Data: %s" % combined_coin

    # Assuming the coin data is base64 encoded, lets decode it
    b64data = b64decode(combined_coin)

    # Lets attempt to decompress this with zlib
    print "Attempting to decompress data..."
    decompressed_data = decompress(b64data)

    # File appaears to be an MP2 file based on the "file" command
    mp2 = decompressed_data


def read_fileline(path):
    with open(path, 'rb') as f:
        return f.read().strip()


if __name__ == "__main__":
    main()
