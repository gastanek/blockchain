'''short routine to test the grpc server services
'''
import grpc, sys
sys.path.insert(0, '../')

from transactionqueue import txnqueue_grpc_pb2
from transactionqueue import txnqueue_grpc_pb2_grpc

import random

txnIdList = []

def sendInTxn(stub):
    #create a random transaction id
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k' 'l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    txnid = ''.join([str(random.randint(0, 9)) for i in range(6)])
    txndata = ''.join([chars[random.randint(1,24)] for i in range(50)]) #generate random 50 char string
    txnIdList.append(txnid)

    txnbits = txnqueue_grpc_pb2.txndata(txnid=txnid, data=txndata, weight=random.randint(1,20))
    retvalue = stub.setTxnInQueue(txnbits)

def longRunTxns(stub):
    #create a random transaction id
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k' 'l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    txnid = ''.join([str(random.randint(0, 9)) for i in range(6)])
    txndata = ''.join([chars[random.randint(1,24)] for i in range(50)]) #generate random 50 char string
    txnbits = txnqueue_grpc_pb2.txndata(txnid=txnid, data=txndata, weight=random.randint(1,20))
    stub.setTxnInQueue(txnbits)


def fetchTxn(stub):
    #fetch the data we just sent in
    #for a in txnIdList:
    a=1
    while a<8:
        inputbits = txnqueue_grpc_pb2.txnrequest(txnid=chr(a), weight=random.randint(1,20))
        msgresponse = stub.getTxnFromQueue(inputbits)
        
        print("Return Message " + str(msgresponse))
        print(str(a))
        a+=1

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = txnqueue_grpc_pb2_grpc.txnQueueInterfaceStub(channel)
    #print("Testing the server.  Sending in transactions:")
    i=0
    while i<5:
        sendInTxn(stub)
        i+=1
    #print("Transactions sent in, fetching data")
    fetchTxn(stub)
    print("Transaction test complete")


def longRun():
    #this is a long running test with randomized amount of txns to be added
    channel = grpc.insecure_channel('localhost:50051')
    stub = txnqueue_grpc_pb2_grpc.txnQueueInterfaceStub(channel)

    try:
        while True:
            longRunTxns(stub)
            time.sleep(random.randint(0,3))
    except KeyboardInterrupt:
        break


if __name__ == '__main__':
    #for i in len(txnIdList):
        #txnIdList.pop(i)    
    run()