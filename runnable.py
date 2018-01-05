'''
Created 12/21/2017 by gastanek
Personal exercise used to demonstrate simple blockchain concepts and proof of work concepts

Source is freely usable by anyone

Note the limitations:
    1) this isn't intended to convey any ideas of transactional saftey and gaurantees
    2) clustering/consensus is not implemented here (yet)

Main Runnable
    - this initiates the entire process
        - start in a separate process a listener/transaction queue
        - initiate the main blockchain process to iterate

'''
'''
Next todos:
    - separate runnable processes for transaction queue and block processing
    - change the mainblock to have two parts, the txn log and the header blockchain with merkle tree
    - change the persistence to write out both parts to disk
    - reverse the steps for hashing the block and persisting the block
    - locking process to keep a successfully hashed block from being updated before it is persisted
    - thread the transaction processing from the hashing and persistence so they can run simultaneously
    - necessary mechanics and locking to ensure ^^^ doesn't suck
    - proces to look up a specific txn in the merkle tree, or index of txns?
    - implement exteranl api for accepting transaction messages
    - modification to transaction queues to use external tool
    - consensus with broadcasting blocks and everything that would be involved here > fetch blocks, orphan blocks, forks
'''


#runnable used testing
from mainblock import mainblock
from hashblock import hashblock
from transactionQueue import transactionQueue
from processBlock import processBlock
import random

#list for storing fake txnids 
txnIdList = []

def createFakeTxn(queue):
    #create a random transaction id
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k' 'l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    txnid = ''.join([str(random.randint(0, 9)) for i in range(6)])
    txndata = ''.join([chars[random.randint(1,24)] for i in range(50)]) #generate random 50 char string
    txnIdList.append(txnid)
    queue.setTxnInQueue(txnid, txndata, random.randint(1,20))


if __name__ == "__main__":
    #kick off the txn server to receive incoming txns
    
    myblock = mainblock("abcdefgh") #initiate with a reference to our 'genisis' block
    
    #load the transaction queue 
    txnMaxCount = 10
    #initiate the queue
    curQueue = transactionQueue()
    i=0
    while i < txnMaxCount:
        createFakeTxn(curQueue)
        i+=1
    
    for key,value in curQueue.txnQueue.items():
        print(str(key))
        print(str(value))
    
    for a in txnIdList:
        message, key, value=curQueue.getTxnFromQueue(a, 0)
        print("Message " + str(message))
        print("Key " + str(key))
        print("Value " + str(value))    
        if message:
            myblock.appendTxn(key + " " + value)
    
    '''Currently this may be backwards, the processBlock calls the hashing of the block, but I may want to 
        reverse this as it would mean I could add transactions to the block while it is in the process of 
        hashing and then finalize the block while simultaneously creating a new one for new transactions.'''
    #now call the hashing
    #pBlock = hashblock(myblock)
    #the block is finalized with the correct nonce, now we need to process it
    processBlock(myblock)

    #after successfully processing we'd be looping back to clear out our current working block and set the previous hash with our new hash