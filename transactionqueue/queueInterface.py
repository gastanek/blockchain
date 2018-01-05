'''
queue interface is the communication channel to the transaction queue

it is the main process entry point for the transactionqueue

it starts the grpc server for sending/getting transactions from the queue
it also regularly polls a service (if provided) to fetch transactions to be added to the queue

It is also responsible for rebuilding the queue on signal: new, out of sync, invalide

'''
from transactionQueue import transactionQueue
from grpc import grpc

def pollForUpdates():
    #go out to find updates for the transactionqueue


if __name__ == '__main__':
    #start the queue and the grpc server 

    #transactionqueue
    currentQueue = transactionQueue()

