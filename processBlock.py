'''
Runnable that processes a block.
Processing a block involves:
    - verifying the block details
    - persisting the block to our choosen store (initially just disk)
    - returns true/false to main thread to indicate success/failure

'''

from mainblock import mainblock
from hashblock import hashblock

# main method to accept the block and process

def processBlock(block):
    blockToProcess = block

    #first we need to validate the chain - check that the prevHash of this block equals the last hash
    #in our simple case we are cheating a bit by just grabbing the last file we wrote and getting the hash
    if hashCheck(blockToProcess):
        
        #now run the hash on the block
        hashedBlock = hashblock(blockToProcess)
        #now that we have a returned hash block, we will capture the first 10 characters as our file name and persist it to disk
        persistBlock(hashedBlock, blockToProcess)


def hashCheck(block):
    #TODO: what could be more clever here is to persist the block with the first 10 chars by the prev hash text and
    # if we cannot oppen the file, then we know this block is out of line
    hashToVerify = str(block.prevhash)[0:10]
    print(str(hashToVerify))
    blockFileCheck = hashToVerify + ".block"
    #if the .block file exists, we assume this is correctly chained. this would be a faulty assumption and is just a hack
    path = blockFileCheck
    try:
        open(path, 'r')
        print("Verified previous block, proceeding.")
        return True
    except IOError:
        print("That block file does not exist.")
        return False
        


def persistBlock(block, blockdata):
    #take the processed block, create a filename, and persist to disk
    #get the first 10 chars in the hash for the file name
    blockfilename = str(block)[0:10] + ".block"

    path = blockfilename
    newBlockFile = open(blockfilename, 'w')
    newBlockFile.write(block)
    #this isn't correct, the blockdata is an object right now, when implement txn processing will change it to raw data plus hash
    newBlockFile.write(str(blockdata))
    #TODO: this is only hacked write now with now checks and validation
    newBlockFile.close()


#main routine for testing only
if __name__ == '__main__':
    #create a block with the previous hash of abcdefgh == first block
    block = mainblock("abcdefgh")
    block.txnSet = ['1233', '1234', '5154', '13512', '15512', '135135', '2351', '23512']
    block.setFinalTime()

    processBlock(block)

