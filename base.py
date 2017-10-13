"""
Base Frame - All the image parsers extend from this, meant for quick scalability.

Notes:

TODO:

"""
import os
import sys


class base():
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

	def from_front(self, n):
		"""Almost works like a pop, but doesn't modify the source, instead keeping track of position"""
		self._img_scrub+=n
		return self.img[self._img_scrub-n:self._img_scrub]  # Return needs to happen after the +=

	@staticmethod
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