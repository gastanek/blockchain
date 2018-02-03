'''
Created 12/21/2017 by gastanek
Personal exercise used to demonstrate simple blockchain concepts and proof of work concepts

Source is freely usable by anyone

Note the limitations:
    1) this isn't intended to convey any ideas of transactional saftey and gaurantees
    2) clustering/consensus is not implemented here (yet)

Main Runnable
    - this initiates the entire process
        - start in a separate process a listener/transaction queue
        - initiate the main blockchain process to iterate

'''


from transactionqueue import txn_server
from blocklogic import currentBlock
from tests import grpcservertest
from blocklogic.globalconfigs import globalconfigs
from concurrent.futures import ProcessPoolExecutor
import sys


#list for storing fake txnids 
txnIdList = []
configs = []
configuration = globalconfigs()

def getConfigs():
    try:
        configfile = open("pblock.conf", 'r')
        configlines = configfile.read().splitlines()
        for line in configlines:
            if line.find("#", 0) == -1:
                #this is a config parameter
                splitline = line.split("=")
                configs.append(splitline)
    except IOError:
        print("Error accessing the config file.  Please check the file exists and restart")
        sys.exit()
        
    #map these configs to our global needs
    for configitem in configs:
        if configitem[0].find("maxblocksize", 0) > -1:
            configuration.setMaxSize(configitem[1])
        if configitem[0].find("blockdir", 0) > -1:
            configuration.setDataDir(configitem[1])
        if configitem[0].find("hashedzerobits", 0) > -1:
            configuration.setZeroBits(configitem[1])
        
    print(str(configuration.datadirectory))
    print(str(configuration.maxsizeofblock))
    print(str(configuration.zerobits))



if __name__ == "__main__":
    #mutliprocess execution
    #for simulation purposes, we need 3 processes running - txn queue, block processing, txn creation
    configuration = globalconfigs()
    getConfigs()
'''
    with ProcessPoolExecutor(max_workers=3) as executor:
        executor.submit(txn_server.run)
        #send in txns
        executor.submit(grpcservertest.longRun)
        executor.submit(currentBlock.run)
        
'''