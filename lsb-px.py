"""
Least Significant Bit By Pixel

Useful stuff:

Notes:

TODO
"Needle in a haystack" find text if not at start
"""
import sys
import base

file = "bird.png"  # Default file, otherwise use args
if len(sys.argv)>1:
	file = sys.argv[1]

parser = base.get_parser(file)

lsb_list = [str(i%2) for i in parser.pixels]
bytes_ = ["".join(lsb_list[i:i+8]) for i in range(0, len(lsb_list), 8)]  # Join into groups of 8
ints = [int(x, 2) for x in bytes_]
chars = [chr(x) for x in ints]

print("Message: ")
print("".join(chars))
print("\nAttributes:"+base.pretty_dict(parser.attr))
