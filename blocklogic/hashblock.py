from mainblock import mainblock
import hashlib
import random

#variable for the number of initial 0 bits to achieve with the hash
obits = 5

hashedblock = ''

def hashblock(block):
    #take the main block, iterate the  nonce until we find one that hashes sha256 with correct # of 0 bits
    currentblock = block

    #hashed is false until obits = 3 is true
    finalized = False

    while not finalized:
        #set a nonce
        currentblock.setNonce(generate_nonce(25))
        #hash the block
        hashedblock = createHashBlock(currentblock)
        #print(hashedblock)

        #check the hashblock
        valCheck = str(hashedblock)[0:obits]
        #create the 0 string length to compare
        checkStr = ''.join(["0" for i in range(obits)])
        if valCheck == checkStr:
            print ("Success in finding hashblock")
            finalized = True

    return hashedblock        
                


def generate_nonce(length):
    #Generate pseudorandom number to be used as a nonce
    return ''.join([str(random.randint(0, 9)) for i in range(length)])    

def createHashBlock(block):
    #temporary hack - concat the object properties into a string to be hashed; object doesn't support buffer API
    #take the block object and convert what is necessary for the block hashing
    
    blockstring=''
    for s in block.merkletree:
        blockstring += str(s)
    blockstring += block.prevhash
    blockstring += str(block.nonce)

    hashed = hashlib.sha256()
    hashed.update(blockstring.encode('utf_16'))
    #hashed.update(str(block).encode('utf_8'))
    return hashed.hexdigest()



"""This is a main init block for testing"""

#if __name__ == "__main__":
    #hold for testing