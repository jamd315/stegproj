"""
Base Frame - Contains different parsing classes, and re-used functions

TODO:

"""
import os
import sys
import zlib


def pretty_dict(the_dict, extra_spaces=2, fill="."):
		"""Make a dict pretty for printing"""
		str_out = "\n"
		max_key = max([len(x) for x in the_dict])
		for key in the_dict:  # Turns out you can't comment on line continuations.
		# This builds the output string by adding the dict key, followed by however
		# many of the fill character it needs, followed by the value, and wraps
		# up each line with a newline character
			str_out+=str(key)\
					+fill*(max_key+extra_spaces-len(str(key)))\
					+str(the_dict[key])+"\n"
		return str_out


def warn(msg, level=0):
		if level is 0:
			print("\n[WARN] "+msg+"\n")
		elif level is 1:
			print("\n[REALLY WARN] "+msg+"\n")
		elif level is 2:
			exit("[CRITICAL] "+msg+"\n")
		else:
			exit("[APOCALYPTICAL]"+msg+"\n"+"Also, check this out because\
			 the warn function was used improperly")


class base:
	"""
	Each image parser extends from here for some uniformity
	"""
	def __init__(self, file):
		self.img = None
		self.pixel_array = None
		self.pixels = None
		self.raw_bytes = bytearray()
		self.file = file
		self._img_scrub = 0
		self.attr = {"file":file}
		assert os.path.exists(self.file), "File not found"
		with open(file, "rb") as f:
			self.img = f.read()

	def from_front(self, n):  # Needs to be a class method
		"""Almost works like a pop, but doesn't modify the source, instead keeping track of position"""
		self._img_scrub+=n
		return self.img[self._img_scrub-n:self._img_scrub]  # Return needs to happen after the +=


class bmpParse(base):
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
	"""
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
		if self.attr["headerField"] != "BM":
			warn("Using OS/2 is not supported")
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


class pngParse(base):
	"""
	PNG Framework - retreive pixel array, get attr, etc.

	Useful stuff
	http://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html
	http://www.libpng.org/pub/png/spec/1.2/PNG-Chunks.html

	TODO:
	Still don't have pixel array from IDAT chunk(s)
	  * Compression?  Maybe after something else, tried zlib with no success
	  * Filter?
	  * Interlace?
	(Maybe?) verify CRC
	"""
	def __init__(self, file="8bitBW.png"):  # This init only contains PNG relevant stuff, see base.__init__ for general stuff
		warn("PNG isn't quite working yet", 1)
		base.__init__(self, file)
		assert file[-4:] == ".png", "File not PNG"
		self.rawChunks = {}
		self.chunkParse()
		self.raw_bytes = zlib.decompress(self.raw_bytes)  # TODO verify this is correct
		
	
	def chunkParse(self):
		fileHead = self.from_front(8)
		assert fileHead == b'\x89PNG\r\n\x1a\n', "invalid png"  # If this fails, not a PNG or very broken
		chunkType = ""  # flag var needs initialization
		while chunkType != "IEND":
			chunkLen = int.from_bytes(self.from_front(4), byteorder="big")
			chunkType = self.from_front(4).decode()
			chunk = self.from_front(chunkLen)
			crc = self.from_front(4)  # Currently this is largely ignored, TODO why not fix this and verify the CRC?
			self.rawChunks.update({chunkType:chunk})  # Store each chunk under its name in a dict
			if chunkType == "IHDR":  # Image header
				self.attr = {
					"file":self.file,
					"width":int.from_bytes(chunk[:4], byteorder="big"),
					"height":int.from_bytes(chunk[4:8], byteorder="big"),
					"bitDepth":chunk[8],
					"colorType":chunk[9],
					"compressionMethod":chunk[10],
					"filterMethod":{"0":"None", "1":"Sub", "2":"Up", "3":"Average", "4":"Paeth"}[str(chunk[11])],
					"interlaceMethod":{"0":"None", "1":"Adam7"}[str(chunk[12])]
				}
				if self.attr["colorType"] is not 0 or self.attr["bitDepth"] not in [1, 2, 4, 8, 16]:
					warn("Not a greyscale, or invalid bit depth")
				if self.attr["interlaceMethod"] is not "None":
					warn("Adam7 interlace detected, currently not supported")
				if self.attr["filterMethod"] is not "None":
					warn("Unknown filter type of "+self.attr["filterMethod"])
			elif chunkType == "IDAT":
				self.raw_bytes += chunk  # So it turns out there can be multiple IDAT chunks, this method facilitates that.
			elif chunkType == "IEND":
				pass  # Just some laziness with the flag var to keep IEND out of the else block
			elif chunkType == "tIME":
				year = str(int.from_bytes(chunk[:2], byteorder="big"))
				month = str(chunk[2]).zfill(2)
				day = str(chunk[3]).zfill(2)
				hour = str(chunk[4]).zfill(2)
				minute = str(chunk[5]).zfill(2)
				second = str(chunk[6]).zfill(2)
				time = year+"-"+month+"-"+day+" "+hour+":"+minute+":"+second
				self.attr.update({"Time":time})
			elif chunkType == "tEXt":
				self.attr.update({"Text":chunk.decode()})
			else:
				warn("Found chunk "+chunkType+" that was not handled.")  # Meant for anciliary chunks


class gifParse(base):
	"""
	GIF framework - retreive pixel array, get attr, etc
	"""
	def __init__(self, file="range.gif"):
		warn("GIF implementation is not ready yet", 2)
		base.__init__(self, file)
		assert file[-4:] == ".gif", "File not GIF"
		magicnum = self.from_front(6)
		if not (magicnum == b"GIF87a" or magicnum == b"GIF89a"):
			warn("Broken magic number", 2)


class tiffParse(base):
	def __init__(self, file="range.tiff"):
		warn("TIFF implementation is not ready yet", 2)


class pgmParse(base):
	def __init__(self, file="range.pgm"):
		base.__init__(self, file)
		assert file[-4:] == .pgm or file[-4:] == .ppm, "Not a pgm?"
		self.getattr()

		def getattr():
			self.from_front()



try:  # genericParse class in here
	from PIL import Image
	import numpy as np
	class genericParse(base):
		"""
		A catch all for image types I haven't worked on yet yet
		"""
		exists=True  # To check later
		def __init__(self, file=""):
			base.__init__(self, file)
			self.PIL_img = Image.open(file)
			self.pixel_array = np.asarray(self.PIL_img)
			self.pixels = [val for sub in self.pixel_array for val in sub]  # Flatten the array
			self.attr.update({"height":self.pixel_array.shape[0], "width":self.pixel_array.shape[1]})
except ModuleNotFoundError:
	warn("PIL or numpy not found, genericParse will not work")


def get_parser(file):
	"""Just makes a decision on what parser to use"""
	if file[-4:] == ".png":
		parser = pngParse(file)
	elif file[-4:] == ".bmp":
		parser = bmpParse(file)
	elif file[-4:] == ".gif":
		parser = gifParse(file)
	elif file[-4:] == ".tif" or file[-4:] == "tiff":
		parser = tiffParse(file)
	elif file[-4:] in [".pgm", ".ppm"]:
		parser = pgmParse(file)
	elif "genericParse" in globals()
		parser = genericParse(file)
		warn("Using generic parser for "+file[-4:])
	else:  # Catch when PIL or numpy not installed
		warn("Couldn't parse this file at all", 2)
	return parser


if __name__ == "__main__":
	os.system("cls")
	if len(sys.argv)>1:
		file = sys.argv[1]
	else:
		warn("Supply base.py with a file please, really only meant to store the classes", 2)

	parser = get_parser(file)
	try:
		print("First 10:"+" ".join([format(x, '#04x') for x in parser.raw_bytes[:10]]))
		print("Last 10: "+" ".join([format(x, '#04x') for x in parser.raw_bytes[-10:]]))
		print()
		print("First 10:"+"|".join(str(bin(x)[2:].zfill(8)) for x in parser.raw_bytes[:10]))
		print("Last 10: "+"|".join(str(bin(x)[2:].zfill(8)) for x in parser.raw_bytes[-10:]))
	except AttributeError:
		warn("No raw_bytes")
	try:
		print("\nAttributes:"+pretty_dict(parser.attr))
	except AttributeError:
		warn("No attributes", 1)