Project to build some of the basic concepts of blockchain.

First references should be:
<a href="https://link.springer.com/article/10.1007/BF00196791">How to timestamp a Digital Document</a>
and
<a href="https://bitcoin.org/bitcoin.pdf">Bitcoin.pdf</a>
which recyclyed the timestamp idea and helped explode the popularity of blockchain.

Also a good read, albeit a mix of bitcoin and blockchain, is the <a href="https://bitcoin.org/en/developer-guide#block-chain">bitcoin developer guide</a>

The project can be run by calling runnable.py 

The 3 main processes can be run separately by running:
1. /transactionqueue/txn_server.py
2. /blocklogic/currentBlock.py
3. /tests/grpcservertest.py

Implemented:
<ul><li>main block class</li>
<li>transaction queue to hold incoming transactions to be processed by the block</li>
<li>grpc server for listening for incoming transactions and serving transactions from the queue to the block</li>
<li>hashing methods to hash the blocks theoretically implementing a proof of work</li>
<li>processing and verifying the blocks are chained together as expected</li>
</ul>

The txn_server will manage the transaction queue.  The grpcservertest will generate fake transactions to send into the transaction queue via the txn_server.  The currentBlock is responsible for pulling transactions off the queue from the txn_server and adding them to the current block.  Once the block is full (in this example we are using max 20 txns, bitcoin max is 1MB) it is sent to be processed.  Processing first verifies the connection to the blockchain by checking the previous hash against the last blockfile, then hashes the current block and persists it to disk (assuming the chain is verified.)  Then a new block is created with the previous hash value set to the hash of the block just hashed.  And the process repeats indefinitely.

