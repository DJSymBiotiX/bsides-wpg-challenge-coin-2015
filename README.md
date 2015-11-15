# BSides Winnipeg 2015 - Challenge Coin #

My solution to the Challenge Coin.

### Challenge ###

At Winnipeg BSides 2015, some participants were given a sweet metal coin. On one side was the logo, and on the other side was a bunch of "random" alphanumeric characters along with some '/' and '+', broken into 4 lines. In the middle of this data was also an image of a clamp with a flag on the inside of it with the letters "QR" inside of it.

### Solution ###

My initial theory was that the alphanumeric data was in base 64 (based on the existence of the '/' and '+' characters), and that it was compressed somehow (based on the clamp image), and that it would somehow be a QR code with the answer on it.

* The first part is manually entering the data from the coin into your computer. This was probably the most challenging part as some characters are slightly ambiguous (1, i, I, l). Fortunately I got it right on my first try.

* Once I got the data in, I started writing up a python program to concatenate the 4 lines and decode them as base64. The result of this (saved into 'coin.zlib-compressed'), was just some binary data.

* Based on my assumption that it was going to be a compressed file, I decided to look at the hex dump to see if I could gather any info from the header. The first bit 0x9C78 apparently indicated that it was using the zlib to compress the data. So I loaded up the zlib library in my python program to decompress the data.

* Upon decompressing the data (saved into 'coin.bin'), the `file` command seemed to indicate that the file was an mp2 file. Looking at the hex dump (with the aid of some friends), we determined that the way the data looked didn't indicate an mp2 file, but an image file instead. All of the hex data in the dump seemed to either be 0, C, F, or 3. All of those hex values indicate 0000, 1100, 1111, and 0011 respectively. This further solidified the theory that it was just a black and white monochrome image.

* We also determined that the amount of bits in the data seemed to indicate a 42x42 square, so we broke up the data in to chunks and printed it out in the console as a 42x42 square using spaces and unicode blocks.

* This seemed to prove our theory that the data was just a monochrome image of a QR Code, but the output seemed too long (vertically) and not a square, so our QR code apps could not read it. We did a little googling, and decided to try to use PIL (Python Image Library) to output some sort of image based on the data.

* After too much time being spent trying to get PIL to work, we eventually got it to output a BMP of the data. It was indeed a QR code, and our phone QR code apps were able to read it and decode it.

* In the QR code was the final solution: 🚩🔜 <-- Also some sort of computer emoji that doesn't seem to print here.

### The End ###

Thanks to JDeuce, Crust, and another person whose name I forget for helping out!