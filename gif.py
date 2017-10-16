import os
import sys
from base import base, gifParse


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
