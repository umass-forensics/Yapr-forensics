__author__ = 'Saksham'

import YaffsParser
import string

def main():
    parser = YaffsParser.get_argparser()
    args = parser.parse_args()

    sorted_blocks = YaffsParser.extract_ordered_blocks(args.imagefile,
                                                       args.chunksize,
                                                       args.oobsize,
                                                       args.blocksize,
                                                       args.tag_offset)

    objects = YaffsParser.extract_objects(sorted_blocks)
    #current_objects = [o for o in objects if not o.is_deleted]

    total_bytes = 0
    total_unique_bytes = 0
    dict_unique_bytes = dict()

    for obj in objects:
        for chunk in obj.chunkDict:
            #dict_unique_bytes.clear()
            for version in obj.chunkDict[chunk]:
                version_tag, version_content = version
                version_bytes = version_content.get_bytes()

                if not version_bytes in dict_unique_bytes:
                    dict_unique_bytes[version_bytes] = len(version_bytes)
                    total_unique_bytes += len(version_bytes)

                total_bytes += len(version_bytes)

    print "The total bytes were: %d\n" % total_bytes
    print "The unique bytes were: %d" % total_unique_bytes
    print "The percentage of unique bytes were: %f" % (total_unique_bytes*100.0/total_bytes)

    pass


if __name__ == '__main__':
    main()