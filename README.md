# BSides Winnipeg 2015 - Challenge Coin #

My solution to the Challenge Coin.

### Challenge ###

At Winnipeg BSides 2015, some participants were given a sweet metal coin. On one side was the logo, and on the other side was a bunch of "random" alphanumeric characters along with some '/' and '+', broken into 4 lines. In the middle of this data was also an image of a clamp with a flag on the inside of it with the letters "QR" inside of it.

![Coin Front](/images/Coin-Front.jpg?raw=true "Coin Front") ![Coin Back](/images/Coin-Back.jpg?raw=true "Coin Back")

### Solution ###

My initial theory was that the alphanumeric data was in base 64 (based on the existence of the '/' and '+' characters), and that it was compressed somehow (based on the clamp image), and that it would somehow be a QR code with the answer on it.

* The first part is manually entering the data from the coin into your computer. This was probably the most challenging part as some characters are slightly ambiguous (1, i, I, l). Fortunately I got it right on my first try. You can see the resulting data below.

        eJwdjjEKRTEIBIW0Qq4i2ApePWAreJWArbA/7y9bDbswGC0A3BiqczbplVXpPN073CZvlatpP5gfbDfK/1JkYfK7q+LSYnoJItRt9R7Lc02CbbPErtfVN/ps4cqVS1sTHNwecmjbSVolihmFwxlJUd0kPVMZIG3B4Ul7ErrXg0NX28mY6k6QjgsGD+HJnh/LpXbz

* Once I got the data in, I started writing up a python program to concatenate the 4 lines and decode them as base64. The result of this (saved into 'coin.zlib-compressed'), was just some binary data. Hex dump shown below.

        0000000 9c78 8e1d 0a31 3145 0408 b485 ae42 d822
        0000010 5e0a 603d 782b 8095 b0ad ef3f 5b2f bb0d
        0000020 1830 002d 18dc 73aa e936 5595 3ce9 3bdd
        0000030 26dc 956f 69ab 983f 6c1f ca37 52ff 6164
        0000040 bbf2 e2ab 62d2 097a d422 f56d cb1e 4d73
        0000050 6d82 c4b3 d7ae 37d5 6cfa cae1 4b95 135b
        0000060 dc1c 721e db68 5a49 8a25 8519 19c3 5149
        0000070 24dd 533d 2019 c16d 49e1 127b d7ba 4383
        0000080 db57 98c9 4eea 8e90 060b e10f 9ec9 cb1f
        0000090 76a5 00f3
        0000093

* Based on my assumption that it was going to be a compressed file, I decided to look at the hex dump to see if I could gather any info from the header. The first bit 0x9C78 apparently indicated that it was using the zlib to compress the data. So I loaded up the zlib library in my python program to decompress the data. Hex dump of decompressed data shown below.

        0000000 fcff cf33 ffff 0cff fff3 00fc c0cf 0fc0
        0000010 3300 30f0 cf03 3fcc fc0c f3f3 c30f 3c3f
        0000020 ccfc cff0 3fcf 3c33 f333 cccf cc3f f3fc
        0000030 0ff3 3ff3 003c c0cc 0fc0 3300 3030 ff03
        0000040 ccfc ffcf ffff 3333 f0ff 0300 000c 0000
        0000050 c300 0000 cfff f3f0 3f33 fcf3 cc3c f0c0
        0000060 303c 0cc3 0f3c 300c 0fc3 c3cf cf0f f303
        0000070 c3f0 c0f3 300f cf0c 03cc 03cc f333 cc33
        0000080 0cff 0cc3 3ff3 30c3 00c0 3c0f ccc0 0300
        0000090 30cf ff33 fcfc ff33 ff3f 0c3f ccff c300
        00000a0 f3cf 00f3 f330 fcfc cccf ffc3 3300 30f3
        00000b0 c0ff fc0c 3ccc f30f 333f 030f cffc fccc
        00000c0 f000 f333 003f 0c3c cf00 fcf0 00c3 fc33
        00000d0 303f fcff 33ff 3ff3 3fff fccc 00c0
        00000dd

* Upon decompressing the data (saved into 'coin.bin'), the `file` command seemed to indicate that the file was an mp2 file. Looking at the hex dump (with the aid of some friends), we determined that the way the data looked didn't indicate an mp2 file, but an image file instead. All of the hex data in the dump seemed to either be 0, C, F, or 3. All of those hex values indicate 0000, 1100, 1111, and 0011 respectively. This further solidified the theory that it was just a black and white monochrome image.

* To determine what size the supposed QR code should be, we counted the total number of bits and did a square root on them (as QR codes should be square) to determine what size the image should be. The number of bits was 1768 to which the square root is 42.04759... This number wasn't perfect, but it was close enough to 42. We also noticed that 42x42 was a standard QR code size, so we went with that.

* Now that we had our size, we broke up the data in to chunks and printed it out in the console as a 42x42 square using spaces and unicode blocks.

* This seemed to prove our theory that the data was definitely a monochrome image of a QR Code, but the output seemed too long (vertically) and not a square, so our QR code apps could not read it. We also determined that the last 4 bits were just padding bits, so the total number of usable bits was actually 1764 which actually had a square root of 42.

* We did a little googling, and decided to try to use PIL (Python Image Library) to output some sort of image based on the data.

* After too much time being spent trying to get PIL to work, we eventually got it to output a BMP of the data. It was indeed a QR code, and our phone QR code apps were able to read it and decode it. The QR Code image can be seen below.

![QR Code](/solution.bmp?raw=true "QR Code")

* In the QR code was the final solution, seen below.

![Final Solution](/images/Solution.jpg?raw=true "Final Solution")

### The End ###

Thanks to JDeuce, Crust, and Dave B for helping out!
