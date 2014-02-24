__author__ = 'wallsr'

from YaffsClasses.YaffsChunk import YaffsHeader
import YaffsParser
import os
import datetime
import sys
import time

import summarize_deleted_blocks


def main():
    parser = YaffsParser.get_argparser()
    args = parser.parse_args()

    print args.imagefile, args.chunksize, args.oobsize, args.blocksize, args.tag_offset
    print "Script started: ", datetime.datetime.now()
    print 'File size: ', os.path.getsize(args.imagefile)

    #read in and order all of the blocks, by reverse order of sequence number
    sorted_blocks = YaffsParser.extract_ordered_blocks(args.imagefile,
                                                       args.chunksize,
                                                       args.oobsize,
                                                       args.blocksize,
                                                       args.tag_offset)



    nonerased_blocks = [b for b in sorted_blocks if not b.is_erased]

    print '%d blocks' % len(sorted_blocks)
    print 'Sequence number range: %d -- %d' \
          % (nonerased_blocks[-1].sequence_num, nonerased_blocks[0].sequence_num)

    print 'Found %d erased blocks.' % (len(sorted_blocks) - len(nonerased_blocks))

    #This can happen if the phone is turned off while writing.
    print 'Found %d blocks with mismatched sequence numbers' \
          % len([block for block in sorted_blocks if block.possible_parse_error])

    missing_seq_nums = summarize_deleted_blocks.get_missing_block_numbers(sorted_blocks)

    objects = YaffsParser.extract_objects(sorted_blocks)

    print 'Found %d objects' % len(objects)
    print 'Found %d objects with a header.' % len([obj for obj in objects if 0 in obj.chunkDict])
    print 'Found %d deleted objects.' % len([obj for obj in objects if obj.is_deleted])

    recent_pairs = []
    total_pairs_count = 0

    for block in sorted_blocks:
        recent_pairs.extend([(tag, chunk) for tag, chunk in block.chunk_pairs if tag.is_most_recent])
        total_pairs_count += len(block.chunk_pairs)

    print 'Number of active chunks: %d' % len(recent_pairs)
    print 'Total number of chunks: %d' % total_pairs_count
    print 'Fraction active: %0.2f' % (float(len(recent_pairs)) / total_pairs_count)

    earliest_atime = sys.maxint
    latest_atime = -sys.maxint

    earliest_mtime = sys.maxint
    latest_mtime = -sys.maxint

    earliest_ctime = sys.maxint
    latest_ctime = -sys.maxint

    #Old blocks are periodically rewritten due to garbage collection
    #and block refreshing; therefore, the oldest chunk might have a
    #high sequence number.
    for block in nonerased_blocks:
        for tag, chunk in block.chunk_pairs:
            if not tag.isHeaderTag:
                continue

            header = YaffsHeader(chunk)

            if header.is_erased:
                continue

            #atime is different in Yaffs than it is in UNIX
            earliest_atime = min(earliest_atime, header.atime)
            latest_atime = max(latest_atime, header.atime)

            earliest_mtime = min(earliest_mtime, header.mtime)
            latest_mtime = max(latest_mtime, header.mtime)

            earliest_ctime = min(earliest_ctime, header.ctime)
            latest_ctime = max(latest_ctime, header.ctime)

    print 'Oldest object atime: %s' % time.ctime(earliest_atime)
    print 'Newest object atime: %s' % time.ctime(latest_atime)

    print 'Oldest object mtime: %s' % time.ctime(earliest_mtime)
    print 'Newest object mtime: %s' % time.ctime(latest_mtime)

    print 'Oldest object ctime: %s' % time.ctime(earliest_ctime)
    print 'Newest object ctime: %s' % time.ctime(latest_ctime)


if __name__ == '__main__':
    main()