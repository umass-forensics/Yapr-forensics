from ypr import utilities

__author__ = 'svarma'


def main():

    parser = utilities.get_argparser();
    args = parser.parse_args();

    sorted_blocks = utilities.extract_ordered_blocks(args.imagefile,
                                                       args.chunksize,
                                                       args.oobsize,
                                                       args.blocksize,
                                                       args.tag_offset);

    nonerased_blocks = [b for b in sorted_blocks if not b.is_erased]
    last_block = nonerased_blocks[0];

    pass

if __name__ == '__main__':
    main()



