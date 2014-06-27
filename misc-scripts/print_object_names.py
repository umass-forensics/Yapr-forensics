from ypr import utilities

__author__ = 'wallsr'

import os


def main():
    parser = utilities.get_argparser()
    parser.add_argument("--write_to_file",
                        help='Write output to file in same directory as image.',
                        action='store_true', default=False, dest="write_to_file")

    args = parser.parse_args()

    if args.write_to_file:
        print args.imagefile

    blocks = utilities.extract_ordered_blocks(args.imagefile,
                                                args.chunksize,
                                                args.oobsize,
                                                args.blocksize,
                                                args.tag_offset)



    objects = utilities.extract_objects(blocks)


    tuple_set = set()

    for object in objects:
        if object.hasNoHeader:
            continue

        for version in object.versions:
            tuple_set.add((object.object_id, version[0][1].name))

    root, ext = os.path.splitext(args.imagefile)

    if args.write_to_file:
        outfile = "%s_object_names.txt" % root
        print 'Outfile: %s' % outfile

        with open(outfile, 'w') as out:
            for tuple in tuple_set:
                out.write(str(tuple) + '\n')
    else:
        for tuple in tuple_set:
            print tuple


if __name__ == '__main__':
    main()