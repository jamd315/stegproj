"""
Generic parser - Use PIL to retreive pixel array

Notes:
Uses third party library, is that allowed?

TODO:
Test this on a computer with python
"""
import os
import sys
from PIL import Image
import numpy as np


class genericParse(base):
	def __init__(self, file=""):
		base.__init__(self, file)
		self.PIL_img = Image.open(file)
		self.pixel_array = np.asarray(self.PIL_img)
		self.pixels = [val for sub in self.pixel_array for val in sub]  # Flatten the array
		self.attr.update({"height":self.pixel_array.shape[0], "width":self.pixel_array.shape[1]})


if __name__ == "__main__":
	os.system("cls")
	if len(sys.argv)>1:
		mygeneric = genericParse(sys.argv[1])
	else:
		mygeneric = genericParse()
	print("First 10:"+" ".join([format(x, '#04x') for x in mygeneric.raw_bytes[:10]]))
	print("Last 10: "+" ".join([format(x, '#04x') for x in mygeneric.raw_bytes[-10:]]))
	print()
	print("First 10:"+"|".join(str(bin(x)[2:].zfill(8)) for x in mygeneric.raw_bytes[:10]))
	print("Last 10: "+"|".join(str(bin(x)[2:].zfill(8)) for x in mygeneric.raw_bytes[-10:]))
	print("\nAttributes:"+genericParse.pretty_dict(mygeneric.attr))
	print()
