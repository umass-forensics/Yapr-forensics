__author__ = 'wallsr'

"""
Given an offset, returns the object id
"""

from YaffsClasses.YaffsOobTag import YaffsOobTag
import YaffsParser


def main():
    parser = YaffsParser.get_argparser()

    parser.add_argument("--offsets", help="Return object ids for these offsets",
                        nargs='*', type=int, dest="offsets")

    args = parser.parse_args()

    print 'input_offset chunk_offset block_seq object_id chunk_id is_header'

    with open(args.imagefile, 'rb') as f:
        for offset in args.offsets:
            chunk_start_offset = offset - (offset % (args.chunksize + args.oobsize))

            f.seek(chunk_start_offset+args.chunksize)
            oob_bytes = f.read(args.oobsize)

            oob = YaffsOobTag(oob_bytes, tag_offset=args.tag_offset)

            print offset, \
                chunk_start_offset, \
                oob.block_seq, \
                oob.object_id, \
                oob.chunk_id, \
                oob.isHeaderTag



if __name__ == '__main__':
    main()