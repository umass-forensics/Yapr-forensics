"""
This script prints the number of unique bytes by comparing different chunks.
"""
from yapr import utilities

__author__ = 'Saksham'

import os


def main():
    parser = utilities.get_argparser()
    parser.add_argument("--map",
                        help="To write a file that maps true chunk offset to their new position in the unique, expired "
                             "chunk image", action="store_true", default=False)
    args = parser.parse_args()

    print args.imagefile

    sorted_blocks = utilities.extract_ordered_blocks(args.imagefile,
                                                     args.chunksize,
                                                     args.oobsize,
                                                     args.blocksize,
                                                     args.tag_offset)


    #We have to extract the objects to set the is_most_recent flag
    #for each of our chunks.
    objects = utilities.extract_objects(sorted_blocks)

    nonerased_blocks = [b for b in sorted_blocks if not b.is_erased]
    blocks = sorted(nonerased_blocks, key=lambda bl: bl.sequence_num)

    #This is a set of byte lists
    unique_set = set()
    unique_pairs = []
    header_count = 0

    for block in blocks:
        for tag, chunk in block.chunk_pairs:
            #We don't care about headers since we won't pass those to DEC0DE
            if tag.isHeaderTag:
                continue

            chunk_bytes = chunk.get_bytes()

            if chunk_bytes not in unique_set:
                unique_pairs.append((tag, chunk))

            unique_set.add(chunk_bytes)

    print 'The total number of unique data chunks: %d' % len(unique_pairs)

    unique_expired = [(tag, chk) for tag, chk in unique_pairs if tag.is_most_recent]

    Write_Chunks_to_file(args.imagefile, unique_expired)

    Write_Offset_map(args.imagefile, unique_expired)

    print 'The total number of unique expired data chunks: %d' % len(unique_expired)

    frac_unique = float(len(unique_expired) * args.chunksize) / os.path.getsize(args.imagefile)

    print 'Fraction of unique-expired-data bytes in image: %0.2f' % frac_unique


def Write_Chunks_to_file(file_name, chunk_pairs):
    """
    This function writes the unique instances of
    expired chunks, on which we plan to run Dec0de
    """
    file_name_parts = file_name.split(".")
    new_file_name = ""
    for i in range(0, len(file_name_parts) - 1):
        new_file_name += file_name_parts[i]
    new_file_name += "_unique_expired_chunks." + file_name_parts[-1]

    f = open(new_file_name, 'wb')
    for (tag, chunk) in chunk_pairs:
        chunk_bytes = chunk.get_bytes()
        f.write(chunk_bytes)
    f.close()


def Write_Offset_map(file_name, unique_expired_chunk_pairs):

    dirs, file_name = os.path.split(file_name)
    root, ext = os.path.splitext(file_name)
    map_file_name = root + "_offset_map.csv"
    complete_path = os.path.join(dirs, map_file_name)

    with open(complete_path, 'w') as outfile:
        unique_expired_file_pos = 0
        for (tag, chunk) in unique_expired_chunk_pairs:
            true_chunk_offset = chunk.offset
            object_name = tag.object_cls.name
            chunk_bytes = chunk.get_bytes()
            outfile.write(str(object_name) + "," + str(true_chunk_offset) + "," + str(unique_expired_file_pos) + "\n")
            unique_expired_file_pos += len(chunk_bytes)


if __name__ == '__main__':
    main()