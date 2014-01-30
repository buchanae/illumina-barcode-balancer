#!/usr/bin/env python3.4

import random
import sys
import statistics
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
