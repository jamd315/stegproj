import os
import sys
from base import base, bmpParse


if __name__ == "__main__":
	os.system("cls")
	if len(sys.argv)>1:
		mybmp = bmpParse(sys.argv[1])
	else:
		mybmp = bmpParse()
	print("First 10:"," ".join([format(x, '#04x') for x in mybmp.raw_bytes[:10]]))
	print("Last 10: "," ".join([format(x, '#04x') for x in mybmp.raw_bytes[-10:]]))
	print()
	print("First 10:"+"|".join(str(bin(x)[2:].zfill(8)) for x in mybmp.raw_bytes[:10]))
	print("Last 10: "+"|".join(str(bin(x)[2:].zfill(8)) for x in mybmp.raw_bytes[-10:]))
	print("\nAttributes:"+bmpParse.pretty_dict(mybmp.attr))