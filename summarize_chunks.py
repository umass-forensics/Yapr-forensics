"""
This script writes important chunk level info. for all chunks to a tsv
"""

__author__ = 'wallsr'

import YaffsParser
import os
import sys
import string


def main():
    parser = YaffsParser.get_argparser()

    args = parser.parse_args()

    root, ext = os.path.splitext(args.imagefile)
    outfile = "%s_chunk_summary.csv" % root

    sys.stderr.write('Ouput file: %s\n' % outfile)

    sorted_blocks = YaffsParser.extract_ordered_blocks(args.imagefile,
                                                       args.chunksize,
                                                       args.oobsize,
                                                       args.blocksize,
                                                       args.tag_offset)

    #We have to make this call to fill out the object specific fields
    objects = YaffsParser.extract_objects(sorted_blocks)

    col_names = "Phone," + \
                "Offset," + \
                "ObjectID," + \
                "ObjectType," + \
                "Filename," + \
                "FileExt," + \
                "IsObjectDeleted," + \
                "ChunkID," + \
                "BlockSeqNum," + \
                "IsHeader," + \
                "IsExpired," + \
                "IsErased," + \
                "Category\n"

    with open(outfile, 'w') as f:
        f.write(col_names)

        for block in sorted_blocks:
            for (tag, chunk) in block.chunk_pairs:
                #Erased chunks won't be part of an object
                if tag.is_erased or block.is_erased:
                    filename = 'NA'
                    ext = 'NA'
                    is_deleted = 'NA'
                    obj_type = 'NA'
                #Check if the object is not a file
                elif tag.object_cls.object_type != 1:
                    filename = _strip_filename(tag.object_cls.name)

                    ext = 'NA'
                    is_deleted = tag.object_cls.is_deleted
                    obj_type = tag.object_cls.object_type
                #Object must be a file
                else:
                    is_deleted = tag.object_cls.is_deleted
                    obj_type = tag.object_cls.object_type
                    filename = _strip_filename(tag.object_cls.name)

                    #Figure out the extension from the filename
                    blah, ext = os.path.splitext(filename)

                    ext = ext if ext != '' else '**NONE**'

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

                line = args.phone_name + "," \
                       + str(chunk.offset) + "," \
                       + str(tag.object_id) + "," \
                       + str(obj_type) + "," \
                       + str(filename) + "," \
                       + str(ext) + "," \
                       + str(is_deleted) + ","\
                       + str(tag.chunk_id) + "," \
                       + str(tag.block_seq) + "," \
                       + str(tag.isHeaderTag) + "," \
                       + str(not tag.is_most_recent) + "," \
                       + str(tag.is_erased) + "," \
                       + str(category) + "\n"

                f.write(line)

    f.close()


def _strip_filename(filename):
    if filename is None or filename == '':
        filename = '**NONE**'
    #Check if we have non-printable chars
    elif not all(c in string.printable for c in filename):
        filename_stripped = ''.join([c for c in str(filename)
                                     if c in string.printable])
        if filename_stripped != filename:
            filename = filename_stripped + "**STRIPPED**"

    return filename


if __name__ == '__main__':
    main()
