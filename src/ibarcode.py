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

import argparse
from enum import Enum
import random

Directions = Enum('left right')

# Read pep 8. Python prefers lowercase)underscore over camelCase

# Generates a random selection of barcodes for our problem (for testing).
# Returns as a list.
def genBarcodes(num, minLength, maxLength):
    # None isn't needed. In fact, you don't even need to call random.seed()
    # random.seed(None)

    alphabet = 'ATCG'
    random_base = lambda: random.choice(alphabet)

    def random_barcode():
        length = random.randint(minLength, maxLength)
        return ''.join(random_base() for i in range(length))

    return [random_barcode() for i in range(num)]


# There must be a better name than "G".
# Don't leave empty braces in a class def.
# class G():
class BarcodeTree:

    # Uppercase and lowercase "n" aren't very meaningful names.
    # Use something like num_to_select and num_barcodes.

    # 'barcodes' is the list of barcodes that go in this group.
    # 'n' indicates the index this group deals with.
    # Increment n after each recursive instantiation.
    # 'N' indicates the max index to group.
    def __init__(self, barcodes, n, N):
        self.barcodes = barcodes
        self.dir = Directions.left

        if n <= N:
            self.terminal = False
            left = []
            right = []

            for barcode in barcodes:
                if barcode[n] in ["A","C"]:
                    left.append(barcode)
                elif barcode[n] in ["G","T"]:
                    right.append(barcode)
                else:
                    # Use exceptions for exceptional cases.
                    # They will give a better, more informative exit.
                    # sys.exit is rarely used in Python programs I've seen.
                    raise ValueError('Malformed barcode: {}'.format(barcode))

            # So, I'm getting slightly complex here,
            # but if you ever wanted to subclass this, you'd run into issues
            # because "G" is hard-coded here. You need a way to get the class
            # to create without hard-coding it. A "classmethod" could work?
            self.leftG = G(left, n + 1, N)
            self.rightG = G(right, n + 1, N)
        else:
            self.terminal = True

    def _opposite_direction(self):
        if self.direction = Directions.right:
            return Directions.left
        else:
            return Directions.right

    def choose(self, parentdir):
        # I actually had to look up the "^"
        # Why did you use XOR? Isn't "or" what you want?
        # direction = self.dir ^ parentdir
        direction = self.dir or parentdir

        # This doesn't read nicely. How can you have "not left"?
        # self.switch_direction() would make more sense.
        #self.dir = not self.dir
        self._switch_direction()

        if self.terminal:
            if self.barcodes:
                return self.barcodes.pop()
            else:
                return None
        else:
            if direction == LEFT:
                return self.leftG.choose(not self.dir)
            elif direction == RIGHT:
                return self.rightG.choose(not self.dir)


# This traverses the list once and is more readable
def min_max(items):
    min_ = float('inf')
    max_ = float('-inf')
    for item in items:
        if item < min_:
            min_ = item
        if item > max_:
            max_ = item
    return min_, max_


def barcodeBalance(barcodes, n, depth=None):
    N = len(barcodes)
    solution = []

    # Can you build a tree without traversing the whole list beforehand?
    # Imagine there were 1 million barcodes, getting the min/max would
    # slow you down.
    minLength, maxLength = min_max(len(barcode) for barcode in barcodes)

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
    return open(file_handle).read().strip().split(',')


# I define my argument parsers on the top level
parser = argparse.ArgumentParser()

parser.add_argument("file", help="The CSV file from which to read the barcodes. All the barcodes should be in one row.")
parser.add_argument("num", help="The number of barcodes to select from the file.")

def main():
    args = parser.parse_args()
    barcodes = parse_file(args.file)
    num = int(args.num)

    # barcodes = genBarcodes(num=400, minLength=6, maxLength=8)
    solution = barcodeBalance(barcodes, num)
    print(solution)


if __name__ == "__main__":
    main()
