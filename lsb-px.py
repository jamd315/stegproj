"""
Least Significant Bit By Pixel

Useful stuff:

Notes:

TODO
"Needle in a haystack" find text if not at start
"""
import sys
from base import base, pngParse, bmpParse, gifParse
try:
	from base import genericParse
except:
	pass

file = "bird.png"
if len(sys.argv)>1:
	file = sys.argv[1]

if file[-4:] == ".png":
	parser = pngParse(file)
elif file[-4:] == ".bmp":
	parser = bmpParse(file)
elif file[-4:] == ".gif":
	parser = gifParse(file)
else:
	try:
		parser = genericParse(file)
		base.warn("Using generic parser for "+file[-4:])
	except ModuleNotFoundError:  # Catch when PIL or numpy not installed
		base.warn("Couldn't parse this file at all", 2)

lsb_list = [str(i%2) for i in parser.pixels]
bytes_ = ["".join(lsb_list[i:i+8]) for i in range(0, len(lsb_list), 8)]  # Join into groups of 8
ints = [int(x, 2) for x in bytes_]
chars = [chr(x) for x in ints]

print("Message: ")
print("".join(chars))
print("\nAttributes:"+parser.pretty_dict(parser.attr))
