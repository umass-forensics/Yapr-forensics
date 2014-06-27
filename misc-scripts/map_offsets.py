__author__ = 'wallsr'

"""
Maps file offsets between files to NAND blocks and pages
"""

import argparse
import sys


def map_offset_to_original(offset, offset_map, filtersize=1024):
    """
    Filter size is the window we use for our bloom filter
    """
    aligned_offset_filter = offset - (offset % filtersize)

    if aligned_offset_filter in offset_map:
        return offset_map[aligned_offset_filter] + (offset % filtersize)
    elif aligned_offset_filter - filtersize in offset_map:
        return offset_map[aligned_offset_filter - filtersize] + (offset % filtersize)

    return None


def map_offset_to_block(offset, blocksize=64, pagesize=2112):
    """
    Blocksize is in pages, pagesize is in bytes.

    If the image contains spare data, include that in the
    blocksize
    """

    page = offset / pagesize
    block = page / blocksize

    return page, block


def read_map_csv(mapfile):
    """

    """

    offset_map = {}

    for line in mapfile.readlines():
        #Skip any comment lines
        if line.startswith('#'):
            continue

        #Line should be something like: '2048,1024'
        orig_offset, new_offset = [int(o) for o in line.split(',')]

        offset_map[new_offset] = orig_offset

    return offset_map


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('mapfile', type=argparse.FileType('r'),
                        help="csv format: offset1, offset2")
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                        help="Defaults to stdin")

    parser.add_argument("-p", "--pagesize",
                        help="The NAND page size (e.g. 2048 bytes). Add spare if file contains oob.",
                        type=int, default=2048)


    args = parser.parse_args()
    offset_map = read_map_csv(args.mapfile)

    print '%d entries in map.' % len(offset_map)

    line = args.infile.readline()

    while line:
        offset = int(line)
        orig_offset = map_offset_to_original(offset, offset_map)

        if orig_offset is None:
            print 'Invalid Offset'
        else:
            print 'Page %d, block %d' % map_offset_to_block(orig_offset, pagesize=args.pagesize)

        line = args.infile.readline()


if __name__ == '__main__':
    main()
