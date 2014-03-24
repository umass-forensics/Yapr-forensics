__author__ = 'Saksham'

import YaffsParser
import os

def main():

    parser = YaffsParser.get_argparser()

    parser.add_argument("-obj_id",
                        help='The object ID of the file whose expired chunks are to be extracted',
                        type=int, dest="obj_id")

    args = parser.parse_args()

    sorted_blocks = YaffsParser.extract_ordered_blocks(args.imagefile,
                                                       args.chunksize,
                                                       args.oobsize,
                                                       args.blocksize,
                                                       args.tag_offset)

    objects = YaffsParser.extract_objects(sorted_blocks)

    chunk_offsets = []
    for obj in objects:
        for tag, chunk in obj.chunk_pairs:
            obj_id = tag.object_id
            if obj_id == args.obj_id:
                is_expired = not tag.is_most_recent
                is_data_chunk = not tag.isHeaderTag

                if is_expired and is_data_chunk:
                    offset = chunk.offset
                    chunk_offsets.append(offset)

    Write_chunks_to_file(args,chunk_offsets)


def Write_chunks_to_file(args, chunk_offsets):

    root, ext = os.path.splitext(args.imagefile)
    root_path = os.path.dirname(args.imagefile)
    out_path = os.path.join(root_path, root + '_expired_data_chunks_obj_' + str(args.obj_id) + ".bin")

    out_ptr = open(out_path, 'wb')

    with open(args.imagefile, 'rb') as res:
        for offset in chunk_offsets:
            res.seek(offset)
            out_ptr.write(res.read(2048))
    out_ptr.close()


if __name__ == '__main__':
    main()
