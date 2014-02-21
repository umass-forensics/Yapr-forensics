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

    objects = YaffsParser.extract_objects(sorted_blocks)

    nonerased_blocks = [b for b in sorted_blocks if not b.is_erased]
    blocks = sorted(nonerased_blocks, key=lambda bl: bl.sequence_num)

    block_times_oldest = [(-sys.maxint)]

    #Each block must have been written before the next block in the sequence
    for block in blocks:
        time_block = -sys.maxint

        for tag, chunk in block.chunk_pairs:
            if not tag.isHeaderTag:
                continue

            header = YaffsHeader(chunk)

            if header.is_erased:
                continue

            #block time is at least as old as the previous block
            #as well as the most recent time for any of its header
            #chunks
            time_block = max(header.ctime, header.atime, header.mtime, time_block)
            print block.sequence_num, \
                time.ctime(header.atime), \
                time.ctime(header.mtime),\
                time.ctime(header.ctime)

        block_times_oldest.append(int(max(time_block, block_times_oldest[-1])))

    #Remove the first item in the list, which we added as -sys.maxint
    block_times_oldest.pop(0)

    #After a chunk expires it isn't moved (I hope). We know a chunk has expired
    #when it is replaced by the most recent chunk for the same object
    #with the same chunk id causing an object header with the modified time
    #A chunk must have been written to the block before it expired. So the chunk's
    #expiration time is an upper bound on when the block was written.
    for block in blocks:
        block.mtime = sys.maxint

        for tag, chunk in block.chunk_pairs:
            obj = tag.object_cls

            if 0 not in obj.chunkDict or tag.is_most_recent:
                continue

            #At worst, the chunk expired by this time.
            if tag.chunk_id > 0:
                mtime = obj.chunkDict[0][0][1].mtime
                tmp = time.ctime(mtime)
                pass
            else:
                mtime = sys.maxint
            #    mtime = obj.chunkDict[0][0][1].ctime

            block.mtime = min(block.mtime, mtime)

    block_times_newest = [b.mtime for b in blocks]



    for block, time_min, time_max in zip(blocks, block_times_oldest, block_times_newest):
        if time_min <= 0:
            time_min_str = '???'
        else:
            time_min_str = time.ctime(time_min)

        if time_max == sys.maxint:
            time_max_str = '???'
        else:
            time_max_str = time.ctime(time_max)

        print '%d\t%s\t%s' % (block.sequence_num, time_min_str, time_max_str)




if __name__ == '__main__':
    main()