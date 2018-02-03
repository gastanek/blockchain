'''
Global configs class to hold program configurations

'''
import time

#configs with defaults

maxsizeofblock = 20
datadirectory = "./blocks"
zerobits = 5


class globalconfigs():

    #Main page for our block
    def __init__(self):
        #nothing to initialize
        print("Intializing PBlock configurations")

    def setMaxSize(self, maxsize):
        self.maxsizeofblock = maxsize

    def setDataDir(self, datadir):
        self.datadirectory = datadir

    def setZeroBits(self, zerobit):
        self.zerobits = zerobit

