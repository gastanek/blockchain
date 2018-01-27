'''
Module to provide an interface for the merkle tree representation of txns in a block

Process:
    Takes a set of transactions and produces the merkle tree representation to be sent back to persist in the block

Validation:
    Provides methods to validate a txn exists in a block and is part of a valid block

'''
import hashlib, random, math

def getMerkleTree(txnset):
    '''
        We'll receive a set of transactions that are going to be persisted to the block
        this will iterate the txnset to produce a merkle tree representation of the blocks
        returns the merkle tree to the caller for persistence
    '''
    returnTree = [] #item 0 is txn count included, then list of txns from base to top, top is the last item so 
                    #returnTree[len(returnTree)-1] = merkle tree root

    for txn in txnset:
        #quite simply hash the txns
        returnTree.append(processHash(txn))

    priorPosition = 0
    position = len(returnTree)
    levels = math.floor(len(txnset)/2)-1  #first level is the hashed txns
    while levels > 0:
        groups = math.ceil((position - priorPosition)/2)
        while groups > 0:
            hash1 = returnTree[priorPosition]
            priorPosition += 1
            if position - priorPosition > 1:
                hash2 = returnTree[priorPosition+1]
                priorPosition += 1
            else:
                hash2 = hash1
            returnTree.append(processHash(hash1 + hash2))
            groups -= 1
        #move the position forward by groups
        position = len(returnTree)
        levels -= 1

    return returnTree

def processHash(txnvalue):
    #simply takes a txn and returns a hash value to the caller

    hashed = hashlib.sha256()
    hashed.update(txnvalue.encode('utf_16'))
    #hashed.update(str(block).encode('utf_8'))
    return hashed.hexdigest()




if __name__ == '__main__':
    #simple runnable for module testing only 

    txnIdList = []
    i=0
    while i < 10:
        #create a random transaction id
        chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k' 'l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        txndata = ''.join([chars[random.randint(1,24)] for a in range(50)]) #generate random 50 char string
        txnIdList.append(txndata)
        i+=1

    print("sample txn list is length " + str(len(txnIdList)))
    hashedTree = getMerkleTree(txnIdList)

    print(str(len(hashedTree)) + " items in the tree")
    for item in hashedTree:
        print(str(item))