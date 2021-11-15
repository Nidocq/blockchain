import json
from time import time

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_trans = []

        # Genesis block is the first block initiated in the chain
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_trans,
            'proof': proof,
            #'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # What is this
        #self.current_trans = []

        self.chain.append(block)
        return block

    def new_trans(self, sender, receiver, amount):
        self.current_trans.append({
            "sender": sender,
            "receiver": receiver,
            "amount:": amount
            })

        return self.last_block()

    def last_block(self):
        return self.chain[-1]

    
