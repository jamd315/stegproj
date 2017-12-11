import os
import sys

file = "range.pgm"

with open(file, "rb") as f:
	raw = f.read()

print(raw.decode())