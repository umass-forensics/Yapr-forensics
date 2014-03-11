"""
This script writes important chunk level info. for all chunks to a tsv
"""

__author__ = 'wallsr'

import YaffsParser
import os
import sys


DEFAULT_PHONE_NAME = "No Name"


def main():
    parser = YaffsParser.get_argparser()

    parser.add_argument('--name',
                        help="The pretty print of the name of the phone whose filesystem is to be parsed. Default: No-Name",
                        type=str, default=DEFAULT_PHONE_NAME, dest="phone_name")

    args = parser.parse_args()

    root, ext = os.path.splitext(args.imagefile)
    outfile = "%s_chunk_summary.tsv" % root

    sys.stderr.write('Ouput file: %s\n' % outfile)

    sorted_blocks = YaffsParser.extract_ordered_blocks(args.imagefile,
                                                       args.chunksize,
                                                       args.oobsize,
                                                       args.blocksize,
                                                       args.tag_offset)

    #We have to make this call to fill out the object specific fields
    objects = YaffsParser.extract_objects(sorted_blocks)

    col_names = "Phone\tOffset\tObjectID\tObjectType\tFilename\tFileExt\tIsObjectDeleted\tChunkID\tBlockSeqNum\tIsHeader\tIsExpired\tIsErased\tCategory\n"

    with open(outfile, 'w') as f:
        f.write(col_names)

        for block in sorted_blocks:
            for (tag, chunk) in block.chunk_pairs:
                filename = tag.object_cls.name

                if filename is None or filename == '':
                    filename = 'NONE'

                #Figure out the extension from the filename
                if filename != 'NONE':
                    blah, ext = os.path.splitext(filename)
                else:
                    ext = 'NONE'



                if tag.is_erased:
                    category = "Erased"
                else:
                    if tag.is_most_recent:
                        if tag.isHeaderTag:
                            category = "Recent header"
                        else:
                            category = "Recent data"
                    else:
                        if tag.isHeaderTag:
                            category = "Expired header"
                        else:
                            category = "Expired data"

                line = args.phone_name + "\t" \
                       + str(chunk.offset) + "\t" \
                       + str(tag.object_id) + "\t" \
                       + str(tag.object_cls.object_type) + "\t" \
                       + str(filename) + "\t" \
                       + str(ext) + "\t" \
                       + str(tag.object_cls.is_deleted) + "\t"\
                       + str(tag.chunk_id) + "\t" \
                       + str(tag.block_seq) + "\t" \
                       + str(tag.isHeaderTag) + "\t" \
                       + str(not tag.is_most_recent) + "\t" \
                       + str(tag.is_erased) + "\t" \
                       + str(category) + "\n"

                f.write(line)

    f.close()


if __name__ == '__main__':
    main()
