"""
PNG Framework - retreive pixel array, get attr, etc.

Useful stuff
http://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html
http://www.libpng.org/pub/png/spec/1.2/PNG-Chunks.html

Notes:

TODO:
Still don't have pixel array from IDAT chunk(s)
  * Compression?  Maybe after something else, tried zlib with no success
  * Filter?
  * Interlace?
(Maybe?) verify CRC
"""
import os
import sys
import zlib
from base import base


class pngParse(base):
	def __init__(self, file="8bitBW.png"):  # This init only contains PNG relevant stuff, see base.__init__ for general stuff
                print("[WARN] PNG isn't quite working yet")
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
					print("[WARN] Not a greyscale, or invalid bit depth")
				if self.attr["interlaceMethod"] is not "None":
					print("[WARN] Adam7 interlace detected, currently not supported")
				if self.attr["filterMethod"] is not "None":
					print("[WARN] Unknown filter type of "+self.attr["filterMethod"])
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
				print("[WARN] Found chunk "+chunkType+" that was not handled.")  # Meant for anciliary chunks


if __name__ == "__main__":
	os.system("cls")
	if len(sys.argv)>1:
		mypng = pngParse(sys.argv[1])
	else:
		mypng = pngParse()
	print("First 10:"+" ".join([format(x, '#04x') for x in mypng.raw_bytes[:10]]))
	print("Last 10: "+" ".join([format(x, '#04x') for x in mypng.raw_bytes[-10:]]))
	print()
	print("First 10:"+"|".join(str(bin(x)[2:].zfill(8)) for x in mypng.raw_bytes[:10]))
	print("Last 10: "+"|".join(str(bin(x)[2:].zfill(8)) for x in mypng.raw_bytes[-10:]))
	print("\nAttributes:"+pngParse.pretty_dict(mypng.attr))
	print()
