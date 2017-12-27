'''
Methods used to gather and cache transaction data that will be added to a block.
Currently this will only fetch the data, cache it for the main routine to process it

Future:
    - this should check/validate the data
    - the set of txn data should be validated/checked to be sure anything already processed isn't readded
    - needs to be able to be blown away to start over

ToDo:
    - needs to be updated so it initiates and manages itself
    - break out the check for specific txns into a separate method

'''
txnQueue ={}

class transactionQueue():
    #main transaction queue block

    def __init__(self):
        #txn queue dictionary
        self.txnQueue = {}

    def setTxnInQueue(self, txnid, data):
        #receive an incoming txn and add it to the queue

        #first check if the txnid is already in our queue
        if txnid not in self.txnQueue:
            #proceed, this is where we'd implement some checks for key, data
            self.txnQueue[txnid] = data
        
        else:
            #txn already is in the queue; nothing to do (although in reality you'd likely want to notify and maybe check values
            # and figure out why a repeated txn showed up.)
            self.txnQueue = self.txnQueue #nothing to do here        

    def getTxnFromQueue(self, txnid):
        #txnid is optional, if not present we return the first txn
        #flag the txnid with an X to denote that it has alrady been fetched but not del from the dict yet
        
        #we return 3 values here, the key, value, and a message to indicate success or failure
        retKey = ''
        retValue = ''
        regMessage = ''

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