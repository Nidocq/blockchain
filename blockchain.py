import json
from time import time
import hashlib
import json
from uuid import uuid4
from textwrap import dedent

from flask import Flask, jsonify, request
from werkzeug.wrappers import response

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

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    #We must recieve reward for finding proof.
    #The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_trans(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    #Forge the new Block by adding it to the chain.
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Created",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])

def new_transactions():

    values = request.get_json()

    #Check that the required fields are in the post'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing value', 400

    # Create a new Transaction
    index = blockchain.new_trans(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transactions will be added to Block {index}'}
    return jsonify(response), 201     

@app.route('/chain', methods=['GET'])

def full_chain():
        response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain)
        }
        return jsonify(response), 200


#Kører nuværende på Manas localhost
if '__name__' == '__main__':
    app.run(host='127.0.0.1', port=5000)