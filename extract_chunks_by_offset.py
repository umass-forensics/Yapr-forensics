__author__ = 'wallsr'

import YaffsParser
import sys


def main():
    parser = YaffsParser.get_argparser()

    parser.add_argument("--offsets",
                        nargs='*', dest="offsets")

    args = parser.parse_args()

    with open(args.imagefile, 'rb') as f:
        for offset in args.offsets:
            f.seek(int(offset))
            sys.stdout.write(f.read(args.chunksize))



if __name__ == '__main__':
    main()