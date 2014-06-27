from ypr import utilities

__author__ = 'wallsr'

"""
This script attempts to figure out the sequence numbers of the deleted blocks


"""


def main():
    parser = utilities.get_argparser()

    args = parser.parse_args()

    #read in and order all of the blocks
    sorted_blocks = utilities.extract_ordered_blocks(args.imagefile,
                                                       args.chunksize,
                                                       args.oobsize,
                                                       args.blocksize,
                                                       args.tag_offset)

    missing_set = get_missing_block_numbers(sorted_blocks)


if __name__ == '__main__':
    main()