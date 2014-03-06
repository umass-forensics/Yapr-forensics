"""
This script writes important chunk level info. for all chunks to a csv
"""

__author__ = 'Saksham'

import YaffsParser
import string

DEFAULT_PHONE_NAME = "No Name"


def main():
    parser = YaffsParser.get_argparser()

    parser.add_argument('--name',
                        help="The pretty print of the name of the phone whose filesystem is to be parsed. Default: No-Name",
                        type=str, default=DEFAULT_PHONE_NAME, dest="phone_name")

    args = parser.parse_args()

    phone_name = args.phone_name

    print args.imagefile

    sorted_blocks = YaffsParser.extract_ordered_blocks(args.imagefile,
                                                       args.chunksize,
                                                       args.oobsize,
                                                       args.blocksize,
                                                       args.tag_offset)

    objects = YaffsParser.extract_objects(sorted_blocks)

    line_seq = []

    for block in sorted_blocks:
        for (tag, chunk) in block.chunk_pairs:
            offset = chunk.offset
            obj_id = tag.object_id
            #obj_type = chunk.obj_type
            chunk_id = tag.chunk_id
            block_id = tag.block_seq
            is_header = tag.isHeaderTag
            is_expired = not tag.is_most_recent
            is_erased = tag.is_erased

            if tag.is_most_recent:
                pass

            if is_erased:
                obj_id = -1
                block_id = -1
                category = "Erased"
            else:
                if not is_expired:
                    if is_header:
                        category = "Recent header"
                    else:
                        category = "Recent data"
                else:
                    if is_header:
                        category = "Expired header"
                    else:
                        category = "Expired data"

            line = phone_name + "\t" + str(offset) + "\t" + str(obj_id) + "\t" + str(chunk_id) + "\t" + str(
                block_id) + "\t" + str(
                is_header) + "\t" + str(is_expired) + "\t" + str(is_erased) + "\t" + str(category)
            line_seq.append(line)

    Write_CSV(line_seq, args.imagefile)


def Write_CSV(line_seq, file_name):
    entire_file = '\n'.join(line_seq)
    col_names = "Phone\tOffset\tObjectID\tChunkID\tBlockSeqNum\tIsHeader\tIsExpired\tIsErased\tCategory"

    file_name_parts = file_name.split(".")
    new_file_name = ""
    for i in range(0, len(file_name_parts) - 1):
        new_file_name += file_name_parts[i]
    new_file_name += "_chunk_summary.tsv"

    f = open(new_file_name, 'w')
    f.write(col_names + "\n" + entire_file)
    f.close()


if __name__ == '__main__':
    main()
