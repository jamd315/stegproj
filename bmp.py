"""
BMP Framework - retreive pixel array, get attr, etc

Useful stuff
https://en.wikipedia.org/wiki/BMP_file_format#File_structure see also examples
https://upload.wikimedia.org/wikipedia/commons/c/c4/BMPfileFormat.png
https://filemonger.com/specs/bmp/wotsit.org/Bmpfrmat/Bmpfrmat.html
https://filemonger.com/specs/bmp/wotsit.org/bmp/BMP.txt

Notes:
Rows are from *bottom to top*, left to right
Little-endian, also called "Intel Format"
Does BMP support BW encoded images?  Looks like image is still RGB

TODO:

"""
import os
import sys
from base import base


class bmpParse(base):
	def __init__(self, file="8bitBW.bmp"):
		base.__init__(self, file)  # This init only contains BMP relevant stuff, see base.__init__ for general stuff
		assert file[-4:] == ".bmp", "Not a bmp"
		self.getattr()  # Attributes will get the offset where the image starts, image is offset through end of file
		self.raw_bytes = self.img[self.attr["offset"]:]
		self.get_pixel_array()
		
	def getattr(self):
		self.attr.update({  # Start with the file header
			"headerField":self.img[:2].decode(),
			"size":int.from_bytes(self.img[2:6], byteorder="little"), # In bytes
			"app01":bytes(self.img[6:8]),  # These two are application specific, almost never used,
			"app02":bytes(self.img[8:10]),
			"offset":int.from_bytes(self.img[10:14], byteorder="little")
		})
		assert self.attr["headerField"] == "BM", "Warning, using OS/2 is not supported"
		DIB_size = int.from_bytes(self.img[14:18], byteorder="little")
		DIB = self.img[18:18+DIB_size]
		self.attr.update({  # Get the data from the DIB header and append to the attributes 
			"DIB_size":DIB_size,
			"width":int.from_bytes(DIB[:4], byteorder="little"),
			"height":int.from_bytes(DIB[4:8], byteorder="little"),
			"colorPlanes":int.from_bytes(DIB[8:10], byteorder="little"),
			"bitDepth":int.from_bytes(DIB[10:12], byteorder="little"),
			"compressionMethod":int.from_bytes(DIB[12:16], byteorder="little"),
			"imageSize":int.from_bytes(DIB[16:20], byteorder="little"),
			"printResH":int.from_bytes(DIB[20:24], byteorder="little"), #pix/meter
			"printResV":int.from_bytes(DIB[24:28], byteorder="little"), #pix/meter
			"colorsInPalette":int.from_bytes(DIB[28:32], byteorder="little"),
			"importantColors":int.from_bytes(DIB[32:36], byteorder="little")
		})
		assert self.attr["compressionMethod"] == 0, "No compression"

	def get_pixel_array(self):
		self.pixel_array = [self.raw_bytes[i:i+self.attr["width"]] for i in range(0, len(self.raw_bytes), self.attr["width"])][::-1]
		self.pixels = b"".join(self.pixel_array)


if __name__ == "__main__":
	os.system("cls")
	if len(sys.argv)>1:
		mypng = bmpParse(sys.argv[1])
	else:
		mypng = bmpParse()
	print("First 10:"," ".join([format(x, '#04x') for x in mybmp.raw_bytes[:10]]))
	print("Last 10: "," ".join([format(x, '#04x') for x in mybmp.raw_bytes[-10:]]))
	print()
	print("First 10:"+"|".join(str(bin(x)[2:].zfill(8)) for x in mybmp.raw_bytes[:10]))
	print("Last 10: "+"|".join(str(bin(x)[2:].zfill(8)) for x in mybmp.raw_bytes[-10:]))
	print("\nAttributes:"+bmpParse.pretty_dict(mybmp.attr))
