import json
from time import time
import hashlib
import json

class Blockchain(object):
    def __init__(self):
        self.chain = [] # current chain of transactions (Verified)
        self.current_trans = [] # Pending transactions that need to be mined (Unverified)

        # Genesis block is the first block initiated in the chain
        self.new_block(previous_hash=1, proof=100)

    # Make a new block with custom proof and hash from previous block
    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_trans,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # What is this
        #self.current_trans = []

        self.chain.append(block)
        return block


    # Add a new transation to the current transaction
    def new_trans(self, sender, receiver, amount):
        self.current_trans.append({
            "sender": sender,
            "receiver": receiver,
            "amount:": amount
            })

        return self.last_block()

    # Get the last block in the current chain
    def last_block(self):
        return self.chain[-1]

    # hash a block
    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest() 

    # Proof that this block is proofed
    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            #print( "Number : {} hash: {}".format(proof, hashlib.sha256("{}{}".format(last_proof, proof).encode()).hexdigest()) )
            proof += 1

        return proof

    # Helper function that
    def valid_proof(self, last_proof, proof):
        guess = "{}{}".format(last_proof, proof).encode()
        hashGuess = hashlib.sha256(guess).hexdigest()
        return hashGuess[:4] == "0000"


blockchain = Blockchain()
#blockchain.new_trans("phillip", "manas", 1000)
#print(hashlib.sha256("10035293".encode()).hexdigest())
#print(blockchain.proof_of_work(100))