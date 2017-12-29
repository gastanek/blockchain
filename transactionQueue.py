'''
Transaction Queue
Class and methods used to gather and cache transaction data that will be added to a block.
The queue holds:
    - Transaction key: hash of the arbitrary id and data we use as a unique id.
    - Transaction id: external source id for the transaction
    - Transaction data: payload of the transaction
    - Transaction weight: optional weight statement that prioritizes the transaction - equivalent to txn fee miners prioritize
    - Insert Timestamp: timestamp of the time the transaction was added to the queue as a secondary prioritization after weight

PendingQueue:
Internal list of transactions that need to be added to the block still.  This transfers the cost of searching for the next transaction from request to insert time

Future:
    - in a high throughput scenario we may consider external caching tools
    - this should check/validate the data
    - the set of txn data should be validated/checked to be sure anything already processed isn't readded
    - needs to be able to be blown away to start over

ToDo:
    - needs to be updated so it initiates and manages itself
    - break out the check for specific txns into a separate method

'''
import hashlib
import time

txnQueue ={}

class transactionQueue():
    #main transaction queue block

    def __init__(self):
        #txn queue dictionary
        self.txnQueue = {}
        self.txnIdList = []
        self.pendingQueue = []

    def setTxnInQueue(self, txnid, data, weight):
        #receive an incoming txn and add it to the queue
        #txnid is an exteranally recognized id - we will hash the id and data to create a internal id signature, this is part of the returned payload
        #txnid will be added to the bloom filter for fast confirmation
        if txnid && data is None:
            return Exception

        #create an internal signature
        hashed = hashlib.sha256()
        hashed.update(txnid.encode('utf_16'))
        hashed.update(data.encode('utf_16'))
        #hashed.update(time.time().encode('utf_16'))
        keySig = hashed.hexdigest()

        #first check if the txnid is already in our queue
        if keySig not in self.txnQueue:
            #proceed, this is where we'd implement some checks for key, data
            #first create the internal transaction signature
            self.txnQueue[keySig] = {'txnid': txnid, 'data': data, 'weight': weight, 'time': time.time()}
            __addToListQueue(keySig, weight)
            #txnIdList.append(txnid)

        else:
            #txn already is in the queue; nothing to do (although in reality you'd likely want to notify and maybe check values
            # and figure out why a repeated txn showed up.)
            self.txnQueue = self.txnQueue #nothing to do here        

    def getTxnFromQueue(self, txnid, minWeight):
        #txnid is optional, if not present we return the first txn
        #the minWeight variable is a positive interger value that the caller provides to create a floor on transactions it would like to process (this is equivalent to the bitcoin txn fee a miner would accept)
        #flag the txnid with an X to denote that it has alrady been fetched but not del from the dict yet
        
        #we return 3 values here, the key, value, and a message to indicate success or failure
        retKey = ''
        retValue = ''
        regMessage = ''

        if minWeight is None:
            minWeight = 0

        #because we need to check for deletions, we can't just get the next iter
        for key, value in txnQueue:        
            if txnid is None:
                #get the first key in the dict not marked for deletion
                if "X" not in key:
                    retKey = key
                    retValue = value
                    retMessage = True
                    #mark the key for deletion
                    txnQueue[str(key)+"X"] = txnQueue.pop[key]
                    break
            else:
                #we are searching for a specific txnid
                if key == txnid:
                    #don't need to check for deletion flag as it is implied
                    #don't need to set the key, we presume they already have it
                    retValue = value
                    retMessage = True
                    txnQueue[str(key)+"X"] = txnQueue.pop[key]
                else:
                    #we didn't find the key, must return an error
                    retMessage = False
                    break            


    def delTxnFromQueue(self, txnid):
        #for "safety" we don't delete the txn right as it is fetched from the queue
        #it is flagged in the txn queue for deletion
        #first append an X to the txnid
        delkey = str(txnid) + "X"
        if delkey in txnQueue:
            del txnQueue[delkey]


    def getQueue(self):
        return self

    def fetchTxnsFromSource(self):
        # this function is for calling an external source for the latest txns that it needs to add it its queue
        # the partner function is an inbound listener for new data to add - for now we are just implementing a calling function 
        return self

    def __addToListQueue(keySig, txweight):
        #interanl function for adding a keySig to our list of items that need to be processed
        #this list is ordered by priority
        for val in pendingQueue:
            if val['weight'] < txweight:
                pos = enumerate(val)
                pendingQUeue.inert(pos, {'key': keySig, 'weight': txweight})
                break
             

