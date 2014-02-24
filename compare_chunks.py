__author__ = 'wallsr'

import YaffsParser

def main():
    parser = YaffsParser.get_argparser()
    args = parser.parse_args()

    #read in and order all of the blocks, by reverse order of sequence number
    sorted_blocks = YaffsParser.extract_ordered_blocks(args.imagefile,
                                                       args.chunksize,
                                                       args.oobsize,
                                                       args.blocksize,
                                                       args.tag_offset)

    objects = YaffsParser.extract_objects(sorted_blocks)

    print 'Extracted %d objects' % len(objects)

    count = 0

    for obj in objects:
        for key in obj.chunkDict:
            #Ignore header chunks, we don't really care why they changed.
            if key == 0:
               continue

            #The number of old chunks
            count += len(obj.chunkDict[key]) - 1
            compare_chunks(obj.chunkDict[key])

    print 'Found %d old chunks' % count

    pass


def compare_chunks(chunks):
    """
    Expects a list of YaffsChunk objects
    """

    for x in xrange(len(chunks)-1):
        first_tag, first_chunk = chunks[x]
        second_tag, second_chunk = chunks[x+1]

        first_bytes = first_chunk.get_bytes()
        second_bytes = second_chunk.get_bytes()

        index = compare_bytes(first_bytes, second_bytes)

        if index is None:
            print 'Tag didn\'t change!'
        else:
            print 'Tags changed...boring: %d' % index

    pass


def compare_bytes(chunk1, chunk2):
    """
    Expects a list of bytes, returns index of first byte that is different
    """

    length = min(len(chunk1), len(chunk2))

    for x in xrange(length):
        if chunk1[x] != chunk2[x]:
            return x

    return None

if __name__ == '__main__':
    main()