'''
Created 12/21/2017 by gastanek
Examples used to demonstrate simple blockchain concepts and expand to show proof of work concepts

Source is freely usable by anyone

Note the limitations:
    1) this isn't intended to convey any ideas of transactional saftey and gaurantees
    2) clustering/consensus is not implemented here
'''

#runnable used testing
from mainblock import mainblock
from hashblock import hashblock

if __name__ == "__main__":
    myblock = mainblock("  ")
    #faketxn = "fake data"
    i=0
    while (i<8):
        myblock.appendTxn(str(i))
        i+=1

    #now call the hashing
    hashblock(myblock)