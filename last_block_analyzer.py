
__author__ = 'svarma'

import YaffsParser

def main():

    parser = YaffsParser.get_argparser();
    args = parser.parse_args();

    sorted_blocks = YaffsParser.extract_ordered_blocks(args.imagefile,
                                                       args.chunksize,
                                                       args.oobsize,
                                                       args.blocksize,
                                                       args.tag_offset);

    nonerased_blocks = [b for b in sorted_blocks if not b.is_erased]
    last_block = nonerased_blocks[0];

    pass

if __name__ == '__main__':
    main()



