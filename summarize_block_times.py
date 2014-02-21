__author__ = 'wallsr'

"""
An object header's ctime should be updated whenever the header is written, so the
ctime should give us an idea of when each block was written. This script will test if the
ctime values make sense based on the block sequence number ordering
"""

import sys
import time

import YaffsParser
from YaffsClasses.YaffsChunk import YaffsHeader


def main():
    parser = YaffsParser.get_argparser()
    args = parser.parse_args()

    print args.imagefile

    #read in and order all of the blocks, by reverse order of sequence number
    sorted_blocks = YaffsParser.extract_ordered_blocks(args.imagefile,
                                                       args.chunksize,
                                                       args.oobsize,
                                                       args.blocksize,
                                                       args.tag_offset)

    nonerased_blocks = [b for b in sorted_blocks if not b.is_erased]
    blocks = sorted(nonerased_blocks, key=lambda bl: bl.sequence_num)

    block_times = [(-sys.maxint)]

    for block in blocks:
        ctime_block = -sys.maxint

        for tag, chunk in block.chunk_pairs:
            if not tag.isHeaderTag:
                continue

            header = YaffsHeader(chunk)

            if header.is_erased:
                continue

            #block time is at least as old as the previous block
            #as well as the most recent ctime for any of its header
            #chunks
            ctime_block = max(header.ctime, header.atime, header.mtime, ctime_block)

        block_times.append(int(max(ctime_block, block_times[-1])))

    #Remove the first item in the list, which we added as -sys.maxint
    block_times.pop(0)

    for block, block_time in zip(blocks, block_times):
        if block_time <= 0:
            print '%d\t???' % block.sequence_num
            continue

        print '%d\t%f\t%s' % (block.sequence_num, block_time, time.ctime(block_time))




if __name__ == '__main__':
    main()