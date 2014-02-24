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

    #Let's grab all of the object headers for newly
    #created objects.
    for obj in objects:
        #make sure the object has at least one header
        if 0 not in obj.chunkDict:
            continue
        #Grab the oldests header for the object
        tag, header = obj.chunkDict[0][-1]

        #We only want to consider file objects
        #also, we want the first header and we know
        #that the number of bytes when the file is
        #created should be 0
        #and that we don't have a time for the block already
        if header.obj_type != 1 \
                or header.is_erased \
                or header.name == 'deleted' \
                or header.name == 'unlinked' \
                or tag.num_bytes > 0:
            continue

        #We'll use mtime. For some phones, the atime
        #takes strange values.
        tag.block_cls.create_times.append(header.mtime)


    nonerased_blocks = [b for b in sorted_blocks if not b.is_erased]
    blocks = sorted(nonerased_blocks, key=lambda bl: bl.sequence_num)

    block_times_list = []

    #Each block must have been written before the next block in the sequence
    for block in blocks:
        #Check if we've already figured out some times
        if len(block.create_times) > 0:
            first = min(block.create_times)
            last = max(block.create_times)
            block_times_list.append((int(first), int(last)))
        else:
            block_times_list.append((None, None))

    #We have to use a new list because so
    #we don't modify the current list. Important
    #when trying to guess the range based on other blocks
    block_times_list_augmented = []

    #if we don't already have a time range for the block,
    #We want to guess the range based on the other blocks
    for x in xrange(len(block_times_list)):
        first, last = block_times_list[x]

        if first is None:
            ran = range(x)

            if ran is None:
                continue

            ran.reverse()

            for y in ran:
                prev_first, prev_last = block_times_list[y]
                if prev_first is not None or prev_last is not None:
                    first = int(max(prev_first, prev_last))
                    break
        if last is None:
            ran = range(x+1, len(block_times_list))
            for z in ran:
                next_first, next_last = block_times_list[z]
                if next_first is not None or next_last is not None:
                    last = int(min(next_first, next_last))
                    break

        block_times_list_augmented.append((first, last))


    for block, (time_min, time_max) in zip(blocks, block_times_list_augmented):
        if time_min is None:
            time_min_str = '???'
        else:
            time_min_str = time.ctime(time_min)

        if time_max is None:
            time_max_str = '???'
        else:
            time_max_str = time.ctime(time_max)

        print '%d\t%s\t%s' % (block.sequence_num, time_min_str, time_max_str)




if __name__ == '__main__':
    main()