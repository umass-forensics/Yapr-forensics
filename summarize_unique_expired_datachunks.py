"""
This script prints the number of unique bytes by comparing different chunks.
"""

__author__ = 'Saksham'

import YaffsParser
import os


def main():
    parser = YaffsParser.get_argparser()
    args = parser.parse_args()

    print args.imagefile

    sorted_blocks = YaffsParser.extract_ordered_blocks(args.imagefile,
                                                       args.chunksize,
                                                       args.oobsize,
                                                       args.blocksize,
                                                       args.tag_offset)

    #We have to extract the objects to set the is_most_recent flag
    #for each of our chunks.
    objects = YaffsParser.extract_objects(sorted_blocks)

    nonerased_blocks = [b for b in sorted_blocks if not b.is_erased]
    blocks = sorted(nonerased_blocks, key=lambda bl: bl.sequence_num)

    #This is a set of byte lists
    unique_set = set()
    unique_pairs = []
    header_count = 0

    for block in blocks:
        for tag, chunk in block.chunk_pairs:
            #We don't care about headers since we won't pass those to DEC0DE
            if tag.isHeaderTag:
                continue

            chunk_bytes = chunk.get_bytes()

            if chunk_bytes not in unique_set:
                unique_pairs.append((tag, chunk))

            unique_set.add(chunk_bytes)

    print 'The total number of unique data chunks: %d' % len(unique_pairs)

    unique_expired = [(tag, chk) for tag, chk in unique_pairs if tag.is_most_recent]

    print 'The total number of unique expired data chunks: %d' % len(unique_expired)

    frac_unique = float(len(unique_expired) * args.chunksize) / os.path.getsize(args.imagefile)

    print 'Fraction of unique-expired-data bytes in image: %0.2f' % frac_unique


if __name__ == '__main__':
    main()