#full regression testable on the blocklist structure
#Tests:
#   - build from scratch
#   - verify list is expected length
#   - add a block and verify list is expected length
#   - get the last block and verify the file can be opened and read
#   - fetch block in list by specific hash and return it's position in the list
#   - Drop/orphan N number of blocks and verify expected length with rebuild and file existence
#   - iterate over 200 times validating list length and existence each time
#       - modulo 20 to validate list



import sys, os, random, shutil
sys.path.insert(0, '../')
from blocklogic.blockList import blockList

def cleanUp():
    try:
        shutil.rmtree("./blocktest")
    except:
        print("Error during clean up, manual clean up required.")

if __name__ == '__main__':

    print("#### Testing the blocklist for expected functionality ###")
    print("---------------------------------------------------------")
    
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k' 'l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9']
    
    #create my fake list of txns
    txnlist = []
    i=0
    while i<100:
        hashForList = ''.join([chars[random.randint(1,34)] for a in range(36)])
        txnlist.append(hashForList)
        if i % 23 == 0:
            savedHashForUseLater = hashForList
        i+=1
    
    print("....")
    try:
        os.mkdir("./blocktest")
    except:
        print("Directory already exists")

    #create my fake list of fake block files for the validation
    for a in txnlist:
        workdir = "./blocktest/" + str(a)[0:15] + ".block"
        newBlockFile = open(workdir, 'w')
        newBlockFile.write("Testing")

    print("fake data and files created - now testing the blocklist")
    print("-------------------------------------------------------")

    theList = blockList("../tests/blocktest")

    print("Rebuilding and verifying the block list")
    print("-------------------------------------------------------")

    theList.rebuildFull(txnlist)

    print("Rebuild successful, sanity check")
    print("-------------------------------------------------------")
    
    if theList.getLength() == 100:
        print("Blocklist length is 100")
    else:
        print("Blocklist lenght is " + theList.getLength() + " which is an unexpected value.")
        print("Exiting now")
        cleanUp()
        sys.exit()

    print("-------------------------------------------------------")
    print("Sanity check passed.  Testing functionality")
    print("-------------------------------------------------------")
    print("Functionality checks proceeding.  Adding new block")

    #new simple block file
    newstring = ''.join([chars[random.randint(1,34)] for a in range(36)])
    workdir = "./blocktest/" + str(newstring)[0:15] + ".block"
    newBlockFile = open(workdir, 'w')
    newBlockFile.write("Testing")

    #now add to list and test
    if not theList.pushBlock(newstring):
        print("Pushing the new blocklist failed.  Exiting")
        cleanUp()
        sys.exit()

    if theList.getLength() != 100:
        Print("Blocklist added but length is now greater than expected value.  Exiting")
        cleanUp()
        sys.exit()

    print("-------------------------------------------------------")
    print("Blockadd passed.  Moving to verifications")
    print("Get the last block")

    lastBlockHash = theList.getLastBlock()
    if len(lastBlockHash) <= 0:
        print("Failed to retrieve the last block hash.  Exiting")
        cleanUp()
        sys.exit()
    
    try:
        workdir = "./blocktest/" + str(lastBlockHash)[0:15] + ".block"
        newBlockFile = open(workdir, 'r')
        testString = newBlockFile.read()
        print("Opened first block file and read value: " + str(testString))
    except IOError:
        print("Failed to locate and open blockfile with file name " + str(lastBlockHash)[0:15] + ".block")
        cleanUp()
        sys.exit()
    
    print("-------------------------------------------------------")
    print("Blockfetch passed.  Moving to fetching block position in list by hash")

    position = theList.getBlockByHash(savedHashForUseLater)
    if not position:
        print("Failed to fetch block by it's hash value.  Exiting")
        cleanUp()
        sys.exit()
    print("Block fetch found.  Position is " + str(position))
    print("-------------------------------------------------------")
    print("Blockfetch by position passed.  Simulating partial rebuild")

    #Drop all blocks from the list that matched the prior position, rebuild new blocks up to position

    newPartialHashList = []
    a = 0
    while a < position:
        hashstring = ''.join([chars[random.randint(1,34)] for j in range(36)])
        newPartialHashList.append(hashstring)
        workdir = "./blocktest/" + str(hashstring)[0:15] + ".block"
        try:
            newBlockFile = open(workdir, 'w')
            newBlockFile.write("Testing")
        except IOError:
            print("IO failure during partial rebuild.")
            cleanUp()
            sys.exit()
        a+=1


    print("Partial rebuild list and file written.  Testing the list now")

    theList.rebuildPartial(position, newPartialHashList)

    if theList.getLength() != 100:
        print("Partial rebuild failed.  List is not equal to 100")

    #now get the last block in the list and validate the file exists and can be opened
    thishashtocheck = theList.getLastBlock()
    workdir = "./blocktest/" + str(thishashtocheck)[0:15] + ".block"
    newBlockFile = open(workdir, 'r')
    strtest = newBlockFile.read()
    
    if len(strtest) <= 0:
        print("Partial list rebuild failed.  getLastBlock returned a block that could not be opened")
        cleanUp()
        sys.exit()

    print("-------------------------------------------------------")
    print("Partial reubuild tests passed.  Moving to regular flow simulation")
    
    i = 0

    while i < 200:
        #we're going to simulate 200 block adds and verifying everything as if this were part of normal processing
        #new hash
        hashstring = ''.join([chars[random.randint(1,34)] for a in range(36)])
        workdir = "./blocktest/" + str(hashstring)[0:15] + ".block"
        newBlockFile = open(workdir, 'w')
        newBlockFile.write("Testing")

        theList.pushBlock(hashstring)

        #verify the last hash is the one we just added
        checkString = theList.getLastBlock()

        if hashstring != checkString:
            print("On the " + str(i) + " iteration we failed to verify the block we just added was the one returned")
            cleanUp()
            sys.exit()

        try:
            workdir = "./blocktest/" + str(checkString)[0:15] + ".block"
            newBlockFile = open(workdir, 'r')
            checkString = newBlockFile.read()
        except IOError:
            print("Failed to open the block file from the last provided hash on the " + str(i) + " iteration.")

        #check the length to be certain it is still 100
        if theList.getLength() > 100:
            print("The list length is now greater than 100 on the " + str(i) + " iteration.")
            cleanUp()
            sys.exit()

        #missing in here is probably a partial rebuild in the middle of a full simulation

        if i%20 == 0:
            print("Full iteration tests passed on the " + str(i) + " iteration.")

        i+=1

    print("-------------------------------------------------------")
    print("All tests passed.  Blocklist performed as expected")
    
    cleanUp()


    

