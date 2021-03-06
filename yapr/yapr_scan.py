"""
This script attempts to determine important characteristics of a Yaffs phone image.

Ideally, this functionality will be incorporated into a new version of the Yaffs parser.
"""

__author__ = 'wallsr'

import argparse
import os

from . import utilities
from .YaffsClasses.YaffsChunk import YaffsHeader
from .YaffsClasses.YaffsOobTag import YaffsOobTag


_description = "attempts to determine important characteristics of the phone image"


def scan_file(image, anchor, chunk_sizes, oob_sizes):
    max_count = 0
    best_csize = None
    best_osize = None
    best_headers = None

    for csize in chunk_sizes:
        for osize in oob_sizes:
            size = os.path.getsize(image)

            #Check if image size is a multiple of the chunk plus oob size.
            if size % (csize + osize) != 0:
                continue

            headers = get_anchor_headers(image, csize, osize, anchor)

            if len(headers) == 0:
                continue

            print ">", csize, osize
            print "Found %d %s headers" % (len(headers), anchor)

            constant_count = count_constant_oobs(image, headers, osize)
            count = 2 * len(headers) - constant_count

            print "Found %d potentially good oobs for the headers." \
                  % (len(headers) - constant_count)

            if count >= max_count:
                max_count = count
                best_csize = csize
                best_osize = osize
                best_headers = headers

    if best_headers is None or len(best_headers) == 0:
        print "Unable to determine sizes."
        return None

    print "Most likely chunk and oob sizes: %d, %d" % (best_csize, best_osize)

    headers = get_anchor_headers(image, best_csize, best_osize, anchor)

    unicode = '.'.join([h.name for h in headers])

    if '\x00' in unicode > 0:
        print "Filenames appear to be in unicode"

    best_oob = guess_oob_offset(image, best_headers, best_osize)

    if best_oob is not None:
        guess_block_size(image, best_csize, best_osize, best_oob)

    return best_osize, best_csize


def count_constant_oobs(image, chunks, oobsize):
    oobs = utilities.get_oob_bytes(image, chunks, oobsize)
    constants_count = 0
    constant = '\xff' * oobsize

    for oob in oobs:
        if oob == constant:
            constants_count += 1

    return constants_count

def guess_oob_offset(image, headers, oob_size):
    oobs_bytes = utilities.get_oob_bytes(image, headers, oob_size)

    best_parsed = []

    # We use -16 because we are looking for 16 bytes in the tag
    # for parsing
    for offset in xrange(0, oob_size-16):
        parsed = []

        for bytes in oobs_bytes:
            parsed_oob = YaffsOobTag(bytes, offset)
            if not parsed_oob.isHeaderTag:
                continue
            else:
                parsed.append(parsed_oob)

        if len(parsed) > len(best_parsed):
            best_offset = offset
            best_parsed = parsed

    object_ids = set([o.object_id for o in best_parsed])

    if len(object_ids) > 0:
        print "OOB tag offset is %d" % best_offset
        print "with %d valid header tags" % len(best_parsed)
        print "Object id: %s" % str(object_ids)
        return best_offset

    print "Unable to determine OOB tag offset."
    return None


def guess_block_size(image, chunk_size, oob_size, oob_offset):
    chunk_pairs = utilities.extract_chunks(image, chunk_size, oob_size)
    chunks = [c for c, o in chunk_pairs[:1024]]

    oobs_bytes = utilities.get_oob_bytes(image, chunks, oob_size)

    oobs = [YaffsOobTag(b, oob_offset) for b in oobs_bytes]

    prev = -1
    counts = []
    count = 0

    for oob in oobs:
        if oob.block_seq != prev:
            if count > 0:
                counts.append(count)
            count = 1
            prev = oob.block_seq
        else:
            count += 1

    import collections
    size, freq = collections.Counter(counts).most_common(1)[0]

    if freq == 1:
        print "Unable to determine block size."
        return None

    print "Most likely block size: %d" % size
    return size


def get_headers(image, chunk_size, oob_size):
    chunk_pairs = utilities.extract_chunks(image, chunk_size, oob_size)

    #First filter, The first byte should be 0x01
    #Litte endian
    header_chunks = [YaffsHeader(c) for c, obb in chunk_pairs
                     if c.get_bytes(4) == '\x01\00\00\00']

    #Now use the second, slower filter.
    header_chunks = [c for c in header_chunks
                     if YaffsHeader(c).is_valid_file()]

    return header_chunks


def get_anchor_headers(image, chunk_size, oob_size, anchor):
    header_chunks = get_headers(image, chunk_size, oob_size)

    anchor_headers = [h for h in header_chunks
                      if h.name.replace('\x00', '') == anchor]

    return anchor_headers


def main():
    """
    Assume we pass this script the image file path as an argument on the
    command line.
    """
    DEFAULT_ANCHORS = ['contacts2.db']
    DEFAULT_CHUNK_SIZES = [2048]
    DEFAULT_OOB_SIZES = [64]

    parser = argparse.ArgumentParser(description=_description)
    parser.add_argument("imagefile", help="The path to the YAFFS2 image.", type=str)
    parser.add_argument("--anchors",
                        help="The filenames to use for anchoring the search. Default: %s" % DEFAULT_ANCHORS,
                        nargs='*', default=DEFAULT_ANCHORS, dest="anchors")
    parser.add_argument("--chunksizes",
                        help="The chunk sizes to test for. Default: %s" % DEFAULT_CHUNK_SIZES,
                        nargs='*', default=DEFAULT_CHUNK_SIZES, dest="chunk_sizes", type=int)
    parser.add_argument("--oobsizes",
                        help="The oob sizes to test for. Default: %s" % DEFAULT_OOB_SIZES,
                        nargs='*', default=DEFAULT_OOB_SIZES, dest="oob_sizes", type=int)
    args = parser.parse_args()

    print args.imagefile

    for anchor in args.anchors:
        print 'Scanning for %s' % anchor
        scan_file(args.imagefile, anchor, args.chunk_sizes, args.oob_sizes)
    pass


if __name__ == '__main__':
    main()
