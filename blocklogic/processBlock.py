'''
Runnable that processes a block.
Processing a block involves:
    - verifying the block details
    - persisting the block to our choosen store (initially just disk)
    - returns true/false to main thread to indicate success/failure

'''

from mainblock import mainblock
from hashblock import hashblock
import sys
sys.path.insert(0, '../')

# main method to accept the block and process

def processBlock(block):
    blockToProcess = block
    #first we need to validate the chain - check that the prevHash of this block equals the last hash
    if hashCheck(blockToProcess):
        
        #now run the hash on the block
        hashedBlock = hashblock(blockToProcess)
        #now that we have a returned hash block, we will capture the first 10 characters as our file name and persist it to disk
        persistBlock(hashedBlock, blockToProcess)
    
        return hashedBlock


def hashCheck(block):
    #take the current block, grab the prevhash, ?get last blok in chain, hash last block and compare
    #how do I know the last block in the chain? not by timestamp? Internal, global structure seems faulty
    #file on disk?
    #if I have a global structure it would need to be rebuilt on restart, how would I know if it is tampered with?
    #what to do at a billion blocks?  Or maybe I could assume I only need the last 100 blocks in an internal structure - 
    #then that probably punts decisions to the consensus 

    #TODO: what could be more clever here is to persist the block with the first 10 chars by the prev hash text and
    # if we cannot oppen the file, then we know this block is out of line
    hashToVerify = str(block.prevhash)[0:15]
    #none of this is correct in that checking file name does not verify previous block
    blockFileCheck = hashToVerify + ".block"
    #if the .block file exists, we assume this is correctly chained. this would be a faulty assumption and is just a hack
    path = "../blocks/" + str(blockFileCheck)
    try:
        open(path, 'r')
        print("Verified previous block, proceeding.")
        return True
    except IOError:
        print("That block file does not exist.")
        return False
    

def persistBlock(block, blockdata):
    #take the processed block, create a filename, and persist to disk
    #get the first 15 chars in the hash for the file name
    blockfilename = str(block)[0:15] + ".block"

    try:
        path = "../blocks/" + str(blockfilename)
        newBlockFile = open(path, 'w')
        newBlockFile.write("Previous Hash: " + block + "\n")

        '''write out the block contents to the file
            txnSet = []
            timestamp = ''
        '''
        newBlockFile.write(str(blockdata.timestamp) + "\n")
        i=0
        for txn in blockdata.txnSet:
            newBlockFile.write(str(i) + " Txn: ")
            newBlockFile.write(str(txn) + "\n")
            i+=1
        newBlockFile.close()
    except:
        print("Critical failure in persisting the block to disk.  Aborting.")
        sys.exit()
    

#main routine for testing only
if __name__ == '__main__':
    #create a block with the previous hash of abcdefgh == first block
    block = mainblock("abcdefghijklmno")
    block.txnSet = ['1233', '12323254', '5124624654', '13512', '15512', '135135', '2351', '23512']
    block.setFinalTime()

    processBlock(block)

