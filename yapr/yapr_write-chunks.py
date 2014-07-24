"""
Writes all of the chunks in the input image to separate files. Each chunk file uses the
naming convention: offset_blockseq_objid_chunkid.dd

"""

__author__ = 'wallsr'

import os
import sys

from . import utilities


_description = """Writes all of the chunks in the input image to separate files. Each chunk file uses the
naming convention: offset_blockseq_objid_chunkid.dd"""


def main():
    parser = utilities.get_argparser()
    args = parser.parse_args()

    sorted_blocks = utilities.extract_ordered_blocks(args.imagefile,
                                                       args.chunksize,
                                                       args.oobsize,
                                                       args.blocksize,
                                                       args.tag_offset)

    nonerased_blocks = [b for b in sorted_blocks if not b.is_erased]

    root, ext = os.path.splitext(args.imagefile)

    root_path = os.path.dirname(args.imagefile)
    out_path = os.path.join(root_path, root + '_chunks')

    print out_path

    if not os.path.exists(out_path):
        os.mkdir(out_path)
    else:
        sys.stderr.write('Warning: chunks directory exists. Overwriting...\n')

    for block in nonerased_blocks:
        for tag, chunk in block.chunk_pairs:
            filename = '%08d_04b%d_obj%04d_%03d.dd' % (chunk.offset,
                                                      tag.block_seq,
                                                      tag.object_id,
                                                      tag.chunk_id)

            with open(os.path.join(out_path, filename), 'wb') as outfile:
                outfile.write(chunk.get_bytes())



if __name__ == '__main__':
    main()