#fake transaction runner
#used in the shortterm to create fake transactions

import time, random
from transactionQueue import transactionQueue

def createFakeTxn(queue):
    #create a random transaction id
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k' 'l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    txnid = ''.join([str(random.randint(0, 9)) for i in range(6)])
    txndata = ''.join([chars[random.randint(1,24)] for i in range(50)]) #generate random 50 char string

    queue.setTxnInQueue(txnid, txndata)
    

if __name__ == '__main__':
    #runnable from this function to test transaction queue 
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
    