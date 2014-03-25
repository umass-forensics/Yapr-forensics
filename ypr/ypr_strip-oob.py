__author__ = 'wallsr'

"""
This simple script removes the OOB bytes from the image.

"""

import os
from optparse import OptionParser


_description = "strip the OOB bytes from the image"


def main():
    """
    Assume we pass this scirpt the image file as an argument
    """

    parser = OptionParser(description=_description)
    parser.add_option('--chunksize', action='store', type='int',
                      dest='chunk_size', default=2048)
    parser.add_option('--oobsize', action='store', type='int',
                      dest='oob_size', default=64)

    options, args = parser.parse_args()

    for image in args:
        print image
        root, ext = os.path.splitext(image)
        outfile = root + "_sans_oob" + ext
        with open(image, 'rb') as f:
            with open(outfile, 'wb') as out:
                while f.read(1) != '':
                    f.seek(-1, True)
                    out.write(f.read(options.chunk_size))
                    f.seek(options.oob_size, True)


if __name__ == '__main__':
    main()