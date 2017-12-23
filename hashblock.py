from mainblock import mainblock
import hashlib
import random

#variable for the number of initial 0 bits to achieve with the hash
obits = 0

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
        print(hashedblock)
        #check the first bits to see what they are
        checkbits = int(hashedblock, 16)
        bits = bin(checkbits)[2:]
        print(str(bits))
        i=0
        while (i<=obits):
            if int(bits)&i !=0:
                #we found a true bit, need to rerun the nonce, recalculate the hash, and check again
                break
            else:
                if i == obits:
                    print("we are done")
                    finalized = True
                i+=1
    
    return hashedblock


def generate_nonce(length):
    #Generate pseudorandom number to be used as a nonce
    return ''.join([str(random.randint(0, 9)) for i in range(length)])    

def createHashBlock(block):
    #temporary hack - concat the object properties into a string to be hashed; object doesn't support buffer API
    blockstring=''
    for s in block.txnSet:
        blockstring += ''.join([str(random.randint(0, 9)) for i in range(5)])
        blockstring += s
    blockstring += block.prevhash

    blockstring += str(block.nonce)

    hashed = hashlib.sha256()
    hashed.update(blockstring.encode('utf_16'))
    return hashed.hexdigest()



"""This is a main init block for testing"""

#if __name__ == "__main__":
    #hold for testing