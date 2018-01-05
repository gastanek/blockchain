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
from transactionQueue import transactionQueue
from processBlock import processBlock

#this is the synthetic cap, in our case it is max number of txns per bock, 1MB in the case of blockchain
maxBlockTxns = 20

def pullTxns(bock):
    #loop indefinitely until we have pulled the max number of txns for this block to be processed
    channel = grpc.insecure_channel('localhost:50051')
    stub = txnqueue_grpc_pb2_grpc.txnQueueInterfaceStub(channel)

    #data, txnid returned
    #a and b can be set to specific txnid and weight, but some value must be passed
    a=''
    b=''

    while i < maxBlockTxns:
        try:
            inputbits = txnqueue_grpc_pb2.txnrequest(txnid=a, weight=b)
            msgresponse = stub.getTxnFromQueue(inputbits)
            if msgresponse.retmessage == "True":
                block.appendTxn(msgresponse)
                i+=1
        except:
            print("Error fethcing txns from the tranaction server to be added to the block")
            break
        

def run():
    #this should be the main loop that is fetching txns and sending the blocks to be processed
    #get our new block
    block = mainblock("abcdefgh") #initiate with a reference to our 'genisis' block
    