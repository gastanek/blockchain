'''
    Main class for a block file queue.
    Function -  maintains the list of the last 100 block files that have been processed and added to the chain
                methods use this to maintain the chain locally and verify blocks before persisting
    List
        blockhash -> hash of block in this position
    limited to 100 items (assumes we'd never branch beyond 100 in the chain and need to roll back more than that)

    methods 
        getLastBlock -> return the last block from the list
        pushBlock(hash) -> pop the 100th and push the 0th
        getBlockByHash(hash) - return position in list of hash passed in - determine how far back it branched
        rebuildPartial(n, list hashes) - n number of first items in the list to drop and then to add with new list
        rebuildFull(list hashes) - complete rebuild from current source - broadcast to the server
        checkRebuild() - after a rebuild, iterate the list and ensure the block files are present
        getLength() - return the length of the current list at any time

    Notes
        - initially this feels like a fundamental weakness in the whole system
        - but we need an internal structure to maintain this instances view of the chain and not just depend on the block files themselves
        - there feels like a lot of assumptions in here, such as
            - simply rebuilding with limited verification of authenticity

'''

hashList = []
datadir = ''

class blockList:

    #Class variables
    hashList = []
    datadir = ''

    #str(block.prevhash)[0:15]

    #Main page for our block
    def __init__(self, datadir):
        self.hashList=[]
        self.datadir = datadir

    def getLastBlock(self):
        #return the last block from our internal list

        return hashList[0]

    def pushBlock(self, hashvalue):
        #add this hashvalue to the list, pop the 100th
        try:
            hashList.pop()
            hashList.insert(0, hashvalue)
            return True
        except:
            return False

    def getBlockByHash(self, hashtofind):
        #return the position of a block in the hash

        try:
            return hashList.index(hashtofind)
        except:
            return

    def rebuildPartial(self, nbr_blocks, newhashlist):
        #partially rebuild the list based on n number of blocks to drop and hashes to add

        del hashList[0:nbr_blocks]

        newhashlist.reverse()

        for a in newhashlist:
            hashList.insert(0, a)

        if self.checkRebuild():
            return True
        else:
            return False
        

    def rebuildFull(self, newhashlist):
        #full rebuild of the hashlist based on a trusted list from another instance
        #ordering is important - reverse through the incoming list to append in order

        hashList.extend(newhashlist)

        if self.checkRebuild():
            return True
        else:
            return False

    def checkRebuild(self):
        #after a rebuild, iterate over our local files and ensure our new list has all the blocks
        #assumes datadir is safe
        for a in hashList:
            try:
                workdir = self.datadir + "/" + str(a)[0:15] + ".block"
                newBlockFile = open(workdir, 'r')
                newBlockFile.read()
            except IOError:
                print("Error: Unable to open bock file associated with hash value in hashList.")
                return False

    def getLength(self):
        return len(hashList)


    