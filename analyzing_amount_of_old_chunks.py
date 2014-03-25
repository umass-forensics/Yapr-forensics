from ypr import utilities

__author__ = 'Saksham'


def main():

    parser = utilities.get_argparser()
    args = parser.parse_args()

    sorted_blocks = utilities.extract_ordered_blocks(args.imagefile,
                                                       args.chunksize,
                                                       args.oobsize,
                                                       args.blocksize,
                                                       args.tag_offset)

    objects = utilities.extract_objects(sorted_blocks)
    #current_objects = [o for o in objects if not o.is_deleted]
    tmp_objects = objects[0:100]

    total_bytes = 0
    older_bytes = 0
    non_header_chunk_versions = 0
    total_chunk_versions = 0

    for obj in objects:
        for chunks in obj.chunkDict:
            for version in obj.chunkDict[chunks]:
                version_len = version[0].num_bytes
                is_old_version = not version[0].is_most_recent
                is_header_chunk = (version[0].chunk_id == 0)

                if not is_header_chunk:
                    non_header_chunk_versions += 1

                if is_old_version and (not is_header_chunk):
                    older_bytes += version_len

                total_bytes += version_len
                total_chunk_versions += 1

    perc_old_bytes = older_bytes * 100.0 / total_bytes
    print "Old chunk bytes that are not header chunks is %f percent" % perc_old_bytes

    pass

if __name__ == '__main__':
    main()






