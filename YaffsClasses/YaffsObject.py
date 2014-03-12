import math
import YaffsChunk

class YaffsObject:

    def __init__(self, obj_id):
        #tuple of type tag, chunk
        self.chunk_pairs = []
        self.object_id = obj_id
        self.versions = []
        self.is_deleted = False
        self.hasNoHeader = False
        self.name = None

        self.object_type = None
        
        #[(tag_cls,chunk_cls)...] tuple lists keyed by chunkId
        #This allows use to have an ordered list of chunks, by id, such
        #that the most recent chunk is first in the list.
        self.chunkDict = {}
        
    def splitByDeletions(self):
        """
        This method will split the object based on the deletion headers.
        We need to do this because object ids are
        reassigned after the old object has been deleted.
        """
        #TODO: I need to take another look at this method.
        splitObjects = []
        
        isFirstIteration = True
        
        obj = None
        
        #iterate through all chunkPairs
        for tag, chunk in self.chunk_pairs:
        
            #if the the tag is a deleted header, then we know this
            # is the start of a new object. Also do this even if
            # the object does not properly start with a header
            isNewObject = (tag.isHeaderTag and tag.isDeleted)
            
            if isNewObject or isFirstIteration:
                obj = YaffsObject(self.object_id)
                splitObjects.append(obj)
                isFirstIteration = False

            obj.chunk_pairs.append((tag, chunk))

        if len(splitObjects) > 1 or len(splitObjects) == 0:
            pass
            
        return splitObjects

    def sanity_check(self):
        """
        This method is a simple sanity check that will return false if any
        of the file versions contain a chunk with a block sequence number
        greater than that of the header chunk. This should not happen as the header
        is always the last part of a file to be written.
        """

        for version in self.versions:
            header_oob, header_chunk = version[0]
            for chunk_id in version:
                if header_oob.block_seq < version[chunk_id][0].block_seq:
                    return False
        return True
        
    def split_by_version(self):
        """
        This method will group the chunk pairs based on object headers.
        Each grouping is called a 'version', and should contain chunks that were
        written after the version's header such that the version doesn't already have
        a chunk with that id and that id does not fall beyond the boundary set by the
        num_bytes field.
        """
        #TODO: It wont handle shrink headers yet.
        #TODO: Doesn't handle issues that arise from missing chunks

        #In the event of an unclean shutdown while the object was open,
        #the first chunk pair (i.e. the last written),
        #won't be a header chunk as expected. If this happens, the current logic
        #always starts with an empty version and assigns a header to it later.
        #This could also happen due to
        #garbage collection
        self.versions = [{}]
        
        for tag, chunk in self.chunk_pairs:
            if tag.isHeaderTag:
                #check if the first version is missing its header
                if len(self.versions) == 1 and 0 not in self.versions[0]:
                    self.versions[0][0] = (tag, chunk)
                #create a new version for this header
                else:
                    chunks = {0: (tag, chunk)}
                    self.versions.append(chunks)
                
            #if this is not a header, add it to every known version that
            # doesn't have a chunk with this id
            #unless this chunk is beyond the end of the file
            else:
                for version in self.versions:
                    #If the version doesn't have a header,
                    #go ahead and add the chunk
                    if 0 not in version:
                        version[tag.chunk_id] = (tag, chunk)
                        continue

                    #The oob tag contains the file size, we shouldn't include
                    # any chunks beyond that file size.
                    filesize = version[0][0].num_bytes
                    num_chunks = int(math.ceil(filesize * 1.0 / chunk.length))
                    if not(tag.chunk_id in version) and tag.chunk_id <= num_chunks:
                        version[tag.chunk_id] = (tag, chunk)

    def reconstruct(self):
        """
        This method should be called after all chunks for the object have been located.
        It will order all previous chunks by chunk id
        """

        for tag, chunk in self.chunk_pairs:
            #It might be useful for tracking which pairs belong to which objects
            tag.object_cls = self

            if tag.isHeaderTag:
                if 0 not in self.chunkDict:
                    self.chunkDict[0] = []

                chunk = YaffsChunk.YaffsHeader(chunk)
                self.chunkDict[0].append((tag, chunk))
            else:
                if tag.chunk_id not in self.chunkDict:
                    self.chunkDict[tag.chunk_id] = []

                self.chunkDict[tag.chunk_id].append((tag, chunk))
        
        if 0 not in self.chunkDict:
            #print 'Object has no header tag!'
            self.hasNoHeader = True
        else:
            tag, chunk = self.chunkDict[0][0]
            self.is_deleted = tag.isDeleted
            self.object_type = chunk.obj_type

            num_chunks = math.ceil(float(tag.num_bytes) / chunk.length)

            for chunk_id in range(int(num_chunks) + 1):
                if chunk_id in self.chunkDict:
                    self.chunkDict[chunk_id][0][0].is_most_recent = True

            #Set the object name
            if not tag.isDeleted:
                self.name = chunk.name
            else:
                names = [x[1].name for x in self.chunkDict[0]
                         if x[1].name not in ['deleted', 'unlinked']]

                if len(names) > 0:
                    self.name = names[0]


    def writeVersion(self, versionNum=0, name=None):
        header, hChunk = self.versions[versionNum][0]
        hChunk = YaffsChunk.YaffsHeader(hChunk)
        
        numChunks = math.ceil(float(hChunk.fsize) / hChunk.length)

        remaining = hChunk.fsize

        if name is None:
            name = hChunk.name

        with open(name, "wb") as f:
            for index in range(int(numChunks)):
                chunk_id = index + 1
                #Versions may be missing certain chunks. This
                #happens due to block erasure.
                if chunk_id not in self.versions[versionNum]:
                    #Make a best effort and grab the most recent
                    #version of that chunk
                    if chunk_id in self.chunkDict:
                        cTag, cChunk = self.chunkDict[chunk_id][0]
                        bytes = cChunk.get_bytes()
                    #otherwise, just write zeroes
                    else:
                        bytes = 0x00 * hChunk.length

                else:
                    cTag, cChunk = self.versions[versionNum][chunk_id]
                    
                    bytes = cChunk.get_bytes()
                    
                if remaining >= len(bytes):
                    f.write(bytes)
                    remaining -= len(bytes)
                else:
                    f.write(bytes[0:remaining])
                    remaining = 0
    
        pass