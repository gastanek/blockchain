#fake transaction runner
#used in the shortterm to create fake transactions locally

import time, random, collections, sys
sys.path.insert(0, '../')

from transactionqueue.transactionQueue import transactionQueue

#list for storing fake txnids 
txnIdList = []

def createFakeTxn(queue):
    #create a random transaction id
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k' 'l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    txnid = ''.join([str(random.randint(0, 9)) for i in range(6)])
    txndata = ''.join([chars[random.randint(1,24)] for i in range(50)]) #generate random 50 char string
    txnIdList.append(txnid)
    queue.setTxnInQueue(txnid, txndata, random.randint(1,20))
    

if __name__ == '__main__':
    #runnable from this function to test transaction queue 
    txnMaxCount = 1
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