#!/usr/bin/env python3.3

'''
Copyright © 2014 Oregon State University
All Rights Reserved.

Permission to use, copy, modify, and distribute this software and its
documentation for educational, research and non-profit purposes, without fee,
and without a written agreement is hereby granted, provided that the above
opyright notice, this paragraph and the following three paragraphs appear in all
copies.

Permission to incorporate this software into commercial products may be obtained
by contacting Oregon State University Office of Technology Transfer.

This software program and documentation are copyrighted by Oregon State
University. The software program and documentation are supplied "as is", without
any accompanying services from Oregon State University. OSU does not warrant
that the operation of the program will be uninterrupted or error-free. The
end-user understands that the program was developed for research purposes and is
advised not to rely exclusively on the program for any reason.

IN NO EVENT SHALL OREGON STATE UNIVERSITY BE LIABLE TO ANY PARTY FOR DIRECT,
INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS,
ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF OREGON
STATE UNIVERSITY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. OREGON
STATE UNIVERSITY SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE AND ANY STATUTORY WARRANTY OF NON-INFRINGEMENT. THE SOFTWARE
PROVIDED HEREUNDER IS ON AN "AS IS" BASIS, AND OREGON STATE UNIVERSITY HAS NO
OBLIGATIONS TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
MODIFICATIONS.
'''

import random
import sys
import argparse
import io
import csv

LEFT = False
RIGHT = True


# Generates a random selection of barcodes for our problem (for testing).
# Returns as a list.
def genBarcodes(num, minLength, maxLength):
	random.seed(None)
	barcodes = []
	for i in range(num):
		barcode = ""
		for j in range(random.randint(minLength, maxLength)):
			barcode += random.choice(["A","G","C","T"])
		barcodes.append(barcode)
	return barcodes


class G():
	# 'barcodes' is the list of barcodes that go in this group.
	# 'n' indicates the index this group deals with.
		# Increment n after each recursive instantiation.
	# 'N' indicates the max index to group.
	#
	#
	def __init__(self, barcodes, n, N):
		self.barcodes = barcodes
		self.dir = LEFT
		if n <= N:
			self.terminal = False
			left = []
			right = []
			for barcode in barcodes:
				if barcode[n] in ["G","C"]:
					left.append(barcode)
				elif barcode[n] in ["A","T"]:
					right.append(barcode)
				else:
					print("Malformed barcodes.")
					sys.exit()
			self.leftG = G(left, n+1, N)
			self.rightG = G(right, n+1, N)
		else:
			self.terminal = True

	def choose(self, parentdir):
		direction = self.dir ^ parentdir
		self.dir = not self.dir
		if self.terminal:
			if self.barcodes != []:
				return self.barcodes.pop()
			else:
				return None
		else:
			if direction == LEFT:
				return self.leftG.choose(not self.dir)
			elif direction == RIGHT:
				return self.rightG.choose(not self.dir)


def barcodeRange(barcodes):
	tmp = [len(x) for x in barcodes]
	return (min(tmp), max(tmp))


def barcodeBalance(barcodes, n, depth=None):
	N = len(barcodes)
	solution = []
	minLength, maxLength = barcodeRange(barcodes)
	if depth == None:
		depth = minLength - 1
	group = G(barcodes, 0, depth)

	i = 0
	while i < n:
		barcode = group.choose(0)
		if barcode != None:
			solution.append(barcode)
			i += 1

	return solution


def parse_file(path):
	csv_array = []
	with open(path, 'r') as file:
		sio_file = io.StringIO(file.read())
	reader = csv.reader(sio_file, delimiter=',')
	for row in reader:
		csv_array.append(row)
	return csv_array[0]


def main():
	parser = argparse.ArgumentParser()

	parser.add_argument("file", help="The CSV file from which to read the barcodes. All the barcodes should be in one row.")
	parser.add_argument("num", help="The number of barcodes to select from the file.")

	args = parser.parse_args()
	barcodes = parse_file(args.file)
	num = int(args.num)

	# barcodes = genBarcodes(num=400, minLength=6, maxLength=8)
	solution = barcodeBalance(barcodes, num)
	print(solution)


if __name__ == "__main__":
    main()
