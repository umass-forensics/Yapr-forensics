__author__ = 'Saksham'

import YaffsParser

def main():

    parser = YaffsParser.get_argparser()
    args = parser.parse_args()

    sorted_blocks = YaffsParser.extract_ordered_blocks(args.imagefile,
                                                       args.chunksize,
                                                       args.oobsize,
                                                       args.blocksize,
                                                       args.tag_offset)

    objects = YaffsParser.extract_objects(sorted_blocks)
    current_objects = [o for o in objects if not o.is_deleted]

    total_bytes = 0
    most_recent_bytes = 0
    non_header_chunk_versions = 0
    total_chunk_versions = 0

    for obj in current_objects:
        for chunks in obj.chunkDict:
            for version in obj.chunkDict[chunks]:
                version_len = version[0].num_bytes
                is_recent_version = version[0].is_most_recent
                is_header_chunk = version[0].chunk_id == 0

                if not is_header_chunk:
                    print "awesome!"
                    non_header_chunk_versions += 1

                if is_recent_version and (not is_header_chunk):
                    most_recent_bytes += version_len

                total_bytes += version_len
                total_chunk_versions += 1

    perc_recent_bytes = most_recent_bytes * 100.0 / total_bytes


    current_objects = current_objects[0:100]
    pass

if __name__ == '__main__':
    main()






