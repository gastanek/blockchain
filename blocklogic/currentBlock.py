'''
This module is the main loop that is grabbing transactions to be added to the block and then
passing the block to be processed and hashed to the blockchain

'''
import grpc, sys
sys.path.insert(0, '../')

from transactionqueue import txnqueue_grpc_pb2
from transactionqueue import txnqueue_grpc_pb2_grpc

from mainblock import mainblock
from hashblock import hashblock
from transactionqueue import transactionQueue
from processBlock import processBlock
from blockList import blockList
import random

#this is the synthetic cap, in our case it is max number of txns per bock, 1MB in the case of blockchain
maxBlockTxns = 20

def pullTxns(block):
    #loop indefinitely until we have pulled the max number of txns for this block to be processed
    channel = grpc.insecure_channel('localhost:50051')
    stub = txnqueue_grpc_pb2_grpc.txnQueueInterfaceStub(channel)
    print("Pulling transactions for the new block.")
    #data, txnid returned
    #a and b can be set to specific txnid and weight, but some value must be passed
    a=1
    b=1
    i=0
    #we will be in this loop until we fill the block that needs to be hashed
    while i < maxBlockTxns:
        #print(str(i) + " is i; maxBlockTxns is " + str(maxBlockTxns))
        try:
            #print("getting the bits")
            #inputbits = txnqueue_grpc_pb2.txnrequest(txnid=chr(a), weight=random.randint(1,20))
            inputbits = txnqueue_grpc_pb2.txnrequest(txnid=chr(a), weight=b)
            #print("trying")
            msgresponse = stub.getTxnFromQueue(inputbits)
            #print(msgresponse)
            if msgresponse.retmessage == "True":
                block.appendTxn(msgresponse)
                i+=1
                print("Transaction " + str(i) + " processed.")
        except Exception as e:
            print(e)
            #print("Error fethcing txns from the tranaction server to be added to the block")
            #break


def run():
    #this should be the main loop that is fetching txns and sending the blocks to be processed
    #get our new block
    block = mainblock("abcdefghijklmno") #initiate with a reference to our 'genisis' block
    blocklist = blockList("../blocks")

    #add transactions to this block until full and ready to be processsed
    try:
        while True:
            #keep looping until we signal it to stop
            pullTxns(block) #put transactions in the block
            hashedblock = processBlock(block) #process the block hash
            blocklist.pushBlock(hashedblock)
            #print(hashedblock)
            block = mainblock(hashedblock) #get a new block with the hash of the old one
            #rinse and repeat until we are told to stop
    except KeyboardInterrupt:
            print("Exiting")

if __name__ == "__main__":
    run()