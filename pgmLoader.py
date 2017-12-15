import os
import sys

file = "bird.pgm"

whitespace = [" ", "\n", "\t", "\r"]

with open(file, "r") as f:
	raw = f.read()

assert raw[:2] == "P2", "Not ASCII grayscale PGM file"
lines = [x for x in raw.split("\n") if "#" not in x[:1]]
width, height = lines[1].split(" ")
width = int(width)
height = int(height)
maxval = lines[2]
img = [x for x in lines[3:] if x is not ""]
lsb = "".join([bin(int(x))[-1] for x in img])
lsb_chunks = [lsb[x*8:(x+1)*8] for x in range(int(len(lsb)/8))]
chars = [chr(int(x, 2)) for x in lsb_chunks]
print(chars)
