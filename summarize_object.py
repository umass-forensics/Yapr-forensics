__author__ = 'wallsr'

"""
The plan is to use this script to help solve the mysteries of object 258.

"""

import YaffsParser


def main():
    parser = YaffsParser.get_argparser()
    parser.add_argument("--object_id", dest='object_id', type=int, default=-1)
    parser.add_argument("--object_name", dest='object_name', default='asd;lfjASDFeofijladksfjoe')
    parser.add_argument("-v", dest='verbose', action="store_true")

    args = parser.parse_args()

    #read in and order all of the blocks, by reverse order of sequence number
    sorted_blocks = YaffsParser.extract_ordered_blocks(args.imagefile,
                                                       args.chunksize,
                                                       args.oobsize,
                                                       args.blocksize,
                                                       args.tag_offset)

    objects_all = YaffsParser.extract_objects(sorted_blocks)


    #objects = [o for o in objects_all if o.object_id == args.object_id]
    objects = []

    #There might be multiple objects with the same ID due to deletions
    for obj in objects_all:

        # Deleted objects might have the name 'deleted'
        # so we need to check past versions
        name_set = set([x[0][1].name for x in obj.versions if 0 in x])

        if obj.object_id == args.object_id or args.object_name in name_set:
            objects.append(obj)

    print 'Found %d object(s).' % len(objects)

    for obj in objects:
        summarize_object(obj, args.verbose)


def summarize_object(target, verbose):
    #We have to use a set here because a block may have multiple chunks for
    #the same object
    block_set = set([tag.block_cls for tag, chunk in target.chunk_pairs])

    #Convert the set back to a sorted list
    blocks = sorted(list(block_set), key=lambda b: b.sequence_num)

    print 'Object %d' %target.object_id
    print 'Num blocks %d' % len(blocks)
    print 'Names: ' + ', '.join(set([x[0][1].name for x in target.versions]))
    print 'Num Chunks: %d' % len(target.chunk_pairs)

    if verbose:
        print "offset\t\tblock_seq\tobj_id\tchunk_id\tnum_bytes\t\tatime\t\tmtime\t\tctime"

        for tag, chunk in target.chunk_pairs:
            output = "%x08\t" % chunk.offset
            output += "%d\t" % tag.block_seq
            output += "%d\t" % tag.chunk_id
            output += "%d\t" % tag.num_bytes

            if tag.isHeaderTag:
                output += "%d\t" % chunk.atime
                output += "%d\t" % chunk.mtime
                output += "%d\t" % chunk.ctime

            print output


    pass




if __name__ == '__main__':
    main()