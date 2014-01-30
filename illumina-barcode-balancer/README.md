## Illumina Barcode Balancer ##

This python program selects a specified number of barcodes from a given input set such that the selected barcodes have as close to a 50/50 ratio of AT / GC as possible, with the ratio importance weighted more to the beginnings of the barcodes.  This ratio is important to ensure proper callibration of Illumina sequencers.

### Usage ###

    usage: ibarcode.py [-h] file num
    
    positional arguments:
        file        The CSV file from which to read the barcodes. All the barcodes
                    should be in one row.
        num         The number of barcodes to select from the file.

    optional arguments:
        -h, --help  show this help message and exit
  
### Example ###

An example file can be found along with the program called lambda.csv.  Run the following with num=10 and verify that your output matches the one shown below.

    $ ./ibarcode.py lambda.csv 10
    ['CGGCCCC', 'AACCGGT', 'CATGGCGC', 'TCTCCGG', 'GGATCG', 'AATACGCG', 'GTGTGC', 'ACGACGCG', 'CCCTAC', 'AAGTAG']

### Requirements ###
Illumina Barcode Balancer was written for Python 3.  It has been tested and confirmed to work in Python 3.3 and Python 3.4.
