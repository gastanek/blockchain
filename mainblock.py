'''
    Main class for a block in our block chain.
    Class variables are
        previoushash -> this is the chained hash from the previous block
        txnSet -> this is the set of transactions that we are accepting within this block, capped at a certain number per block
        nonce -> expanded use, the nonce is what we'll use to do our proof of work
        timestap -> timestamp the block was committed to the chain

    What we will persist is two blocks
        1) is the validated block in the chain which includes the merkel tree
        2) is the list of transactions that are included in this block
'''
import time

class mainblock():

    #Random ceiling on the maximum number of txns per block
    maxTxns = 8
    #array of transactions to be held.  in our case, this can be anything added to the set
    #it doesn't need to be coin transactions exclusively
    txnSet = []
    timestamp = ''

    #Main page for our block
    def __init__(self, prevhash):
        self.prevhash=prevhash

    def appendTxn(self, txndata):
        if len(self.txnSet) < self.maxTxns:
            #take the current txn and add it to our set of txns for this block
            self.txnSet.append(txndata)
        else:
            return str("Block needs to be hashed")
            #for now we will keep this simple
                    
    def setNonce(self, noncevalue):
        self.nonce = noncevalue

    def setFinalTime(self):
        self.timestamp = time.time()
