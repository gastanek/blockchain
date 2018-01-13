'''
txn-server for the transaction queue
'''


from concurrent import futures
import time
import math
import grpc


from transactionQueue import transactionQueue
import txnqueue_grpc_pb2
import txnqueue_grpc_pb2_grpc

currentqueue = ''

class TxnServer(txnqueue_grpc_pb2_grpc.txnQueueInterfaceServicer):
    '''Methods to implement the txn queue server services'''

    def __init__(self):
        #in case we need to init any values
        #need to get passed reference to the curqueue
        #self.globalqueue=currentqueue
        self = self

    def setTxnInQueue(self, request, context):
    #    , txnid, data, weight):
        txnid=request.txnid
        data=request.data
        weight=request.weight
        try:
            print("processing transaction: " + str(txnid) + str(data) + "  " + str(weight))
            returnVal = currentqueue.setTxnInQueue(txnid, data, weight)
            return txnqueue_grpc_pb2.retmessage(rmessage=returnVal)
            #globalqueue.setTxnInQueue(txnid, data, weight)
             
        except Exception as e:
            print(e)
            print("failed transaction")
            return txnqueue_grpc_pb2.retmessage(rmessage='False')

    def getTxnFromQueue(self, request, context):
    #(txnid, weight):
        txnid=request.txnid
        weight=request.weight
        try:
            txnmessage, txnid, value = currentqueue.getTxnFromQueue(txnid, weight)
            print(txnmessage.retmessage)
            return txnqueue_grpc_pb2.txnresponse(retmessage=txnmessage, id=txnid, data=value)
        except Exception as e:
            print(e)
            print('failed to retrieve this thang')
            return txnqueue_grpc_pb2.txnresponse(retmessage="False", id="", data="")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    #txnqueue_grpc_pb2_grpc.add_txnQueueInterfaceServicer_to_server(TxnServer(), server)
    txnqueue_grpc_pb2_grpc.add_txnQueueInterfaceServicer_to_server(TxnServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
            server.stop(0)

def run():
    currentqueue = transactionQueue()
    serve()
    
if __name__ == '__main__':
    currentqueue = transactionQueue()
    serve()
    