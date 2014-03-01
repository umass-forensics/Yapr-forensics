__author__ = 'wallsr'

"""
The plan is to use this script to help solve the mysteries of object 258.

"""

import YaffsParser


def main():
    parser = YaffsParser.get_argparser()
    parser.add_argument("--object_id", dest='object_id', type=int)

    args = parser.parse_args()

    #read in and order all of the blocks, by reverse order of sequence number
    sorted_blocks = YaffsParser.extract_ordered_blocks(args.imagefile,
                                                       args.chunksize,
                                                       args.oobsize,
                                                       args.blocksize,
                                                       args.tag_offset)

    objects_all = YaffsParser.extract_objects(sorted_blocks)

    #There might be multiple objects with the same ID due to deletions
    objects = [o for o in objects_all if o.object_id == args.object_id]

    for obj in objects:
        summarize_object(obj)


def summarize_object(target):
    #We have to use a set here because a block may have multiple chunks for
    #the same object
    block_set = set([tag.block_cls for tag, chunk in target.chunk_pairs])

    #Convert the set back to a sorted list
    blocks = sorted(list(block_set), key=lambda b: b.sequence_num)

    pass




if __name__ == '__main__':
    main()