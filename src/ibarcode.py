#!/usr/bin/env python3.3
# Notes: ^ don't point to a specific version of python.
#          i.e. what if they have only python 3.4?

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
import itertools
import random

Directions = Enum('left right')

# Notes: Check out pep 8. Python prefers lowercase/underscore over camelCase.

# Notes: I turned this into an infinite generator.
def random_barcodes(min_length, max_length):
    """
    Return a list of random barcodes.

    Returns "num" barcodes with a length between "min_length" and "max_length".
    """
    # Notes: You don't need to call random.seed()
    #        unless you want a specific seed.
    # random.seed(None)

    alphabet = 'ATCG'
    random_base = lambda: random.choice(alphabet)

    def random_barcode():
        length = random.randint(min_length, max_length)
        return ''.join(random_base() for i in range(length))

    while True:
        yield random_barcode()


# Notes: "BarcodeTree" is much more descriptive than "G"
#         Also, don't leave empty braces after your class def.
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
                # Notes: strings are sequences, so you can do:
                #        assert 'A' in 'AT'
                if barcode[n] in 'AC':
                    left.append(barcode)
                elif barcode[n] in 'GT':
                    right.append(barcode)
                else:
                    # Notes:
                    # Use exceptions for exceptional cases.
                    # They will give a better, more informative exit.
                    # sys.exit is rarely used in Python programs I've seen.
                    raise ValueError('Malformed barcode: {}'.format(barcode))

            # Notes:
            # So, I'm getting slightly esoteric here,
            # but if you ever wanted to subclass this, you'd run into issues
            # because "BarcodeTree" is hard-coded here.
            # You need a way to get the class to create without hard-coding it.
            # A "classmethod" could work?
            self.left = BarcodeTree(left, n + 1, N)
            self.right = BarcodeTree(right, n + 1, N)
        else:
            self.terminal = True

    def _opposite_direction(self):
        if self.direction = Directions.right:
            return Directions.left
        else:
            return Directions.right

    def choose(self, parentdir=Directions.left):
        # Notes:
        # I actually had to look up the "^"
        # Why did you use XOR? Isn't "or" what you want?
        # direction = self.dir ^ parentdir
        direction = self.direction or parentdir

        # Notes: I think "opposite direction" is more obvious than "not left"
        self.direction = self._opposite_direction()

        if self.terminal:
            if self.barcodes:
                return self.barcodes.pop()
            else:
                return None
        else:
            next_direction = self._opposite_direction()
            if direction == Directions.left:
                return self.left.choose(next_direction)
            elif direction == Directions.right:
                return self.right.choose(next_direction)


# Notes: This traverses the list once and is more readable
def min_max(items):
    min_ = float('inf')
    max_ = float('-inf')
    for item in items:
        if item < min_:
            min_ = item
        if item > max_:
            max_ = item
    return min_, max_


def balance_barcodes(barcodes, n, depth=None):
    # Notes: it's easy to get capital "N" confused with lowercase "n"
    #        descriptive names are better.
    num_barcodes = len(barcodes)
    solution = []

    # Notes:
    # Can you build a tree without traversing the whole list beforehand?
    # Imagine there were 1 million barcodes, getting the min/max would
    # slow you down.
    min_length, max_length = min_max(len(barcode) for barcode in barcodes)

    # Notes: use "variable is None" instead of "variable == None"
    if depth is None:
        depth = min_length - 1

    tree = BarcodeTree(barcodes, 0, depth)

    # TODO move to BarcodeTree.__iter__
    i = 0
    while i < n:
        barcode = tree.choose()
        if barcode != None:
            solution.append(barcode)
            i += 1

    return solution


def parse_barcodes_file(path):
    return open(path).read().strip().split(',')


# Notes: I define my argument parsers on the top level
#        but that's really just a minor style thing.
parser = argparse.ArgumentParser()

parser.add_argument("file", help="The CSV file from which to read the barcodes. All the barcodes should be in one row.")
parser.add_argument("num", help="The number of barcodes to select from the file.")

if __name__ == "__main__":
    args = parser.parse_args()
    num = int(args.num)

    barcodes = parse_barcodes_file(args.file)

    # barcodes_generator = random_barcodes(6, 8)
    # barcodes = itertools.islice(barcodes_generator, num)

    solution = balance_barcodes(barcodes, num)
    print(solution)
