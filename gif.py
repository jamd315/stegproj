"""
GIF framework - retreive pixel array, get attr, etc

Notes:

TODO:

"""
import os
import sys
from base import base


class gifParse(base):
	def __init__(self, file="range.gif"):
		base.__init__(self, file)
		assert file[-4:] == ".gif", "File not GIF"
		magicnum = self.from_front(6)
		assert magicnum == b"GIF87a" or magicnum == b"GIF89a", "Broken magic number"
		


if __name__ == "__main__":
	os.system("cls")
	if len(sys.argv)>1:
		mygif = gifParse(sys.argv[1])
	else:
		mygif = gifParse()
	print("First 10:"+" ".join([format(x, '#04x') for x in mygif.raw_bytes[:10]]))
	print("Last 10: "+" ".join([format(x, '#04x') for x in mygif.raw_bytes[-10:]]))
	print()
	print("First 10:"+"|".join(str(bin(x)[2:].zfill(8)) for x in mygif.raw_bytes[:10]))
	print("Last 10: "+"|".join(str(bin(x)[2:].zfill(8)) for x in mygif.raw_bytes[-10:]))
	print("\nAttributes:"+gifParse.pretty_dict(mygif.attr))
	print()
