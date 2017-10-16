import os
import sys


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
