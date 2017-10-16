import os
import sys
import zlib
from base import base, pngParse


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
