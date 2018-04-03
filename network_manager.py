from flask import Flask, abort, request
from threading import Lock
from timeit import default_timer as timer
import argparse

from block import Block
from block_chain import BlockChain
from serializer import Serializer
from transaction_manager import TransactionManager

# flask init
app = Flask(__name__)
app.secret_key = 'super secret key'

# objects init
mutex = Lock()
s = Serializer()
block_chain = BlockChain()
transaction_manager = TransactionManager()

# create genesis block
genesis_block = Block(index=0,
                    timestamp=timer(),
                    transactions=transaction_manager.get_transactions(),
                    previous_hash="genesis_block",
                    difficulty=block_chain.get_difficulty())
block_chain.set_working_block(genesis_block)


@app.route('/', methods=['GET']) 
def main():
    return block_chain.to_html()


@app.route('/get_block', methods=['GET']) 
def get_block():
    return s.serialize(block_chain.get_working_block())


@app.route('/make_transaction', methods=['POST']) 
def make_transaction():
    if "transaction" not in request.form:
        return ""
    else:
        transactions = s.deserialize(request.form["transaction"])
        transaction_manager.add_transactions(transactions)
        return "Worked!"


@app.route('/collect_transactions', methods=['POST']) 
def collect_transactions():
    if "public_key" not in request.form:
        return ""
    else:
        valid_transactions = block_chain.get_valid_transactions(request.form["public_key"])
        return s.serialize(valid_transactions)


@app.route('/register_miner', methods=['POST']) 
def register_miner():
    if "public_key" not in request.form and "pseudonym" not in request.form:
        return 'Send the right parameters: "public_key" and "pseudonym"'
    else:
        public_key = request.form["public_key"]
        pseudonym = request.form["pseudonym"]
        block_chain.create_wallet(public_key)
        block_chain.add_pseudonym(pseudonym, public_key)
        return ""


@app.route('/resolve_pseudonym', methods=['POST']) 
def resolve_pseudonym():
    if "pseudonym" not in request.form:
        return ""
    else:
        pseudonym = request.form["pseudonym"]
        public_key = block_chain.resolve_pseudonym(pseudonym)
        return public_key


@app.route('/post_block', methods=['POST']) 
def post_block():
    if "block" not in request.form:
        return 'Send the right parameters: "block"'
    else:
        block_string = request.form["block"]
        block = s.deserialize(block_string)

        if block.try_nonce():
            mutex.acquire()

            # Add block to block chain
            block_chain.add_block(block)

            # Prepare next block
            transaction_manager.dump_transactions()
            block_chain.set_working_block(Block(index=block.index + 1,
                                          timestamp=timer(),
                                          transactions=transaction_manager.get_transactions(),
                                          previous_hash=block.hash,
                                          difficulty=block_chain.get_difficulty()))
            mutex.release()
            return ""
        else:
            return "Don't cheat! Only send mined blocks..."


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=5000, help='The port for the network manager')
    args = parser.parse_args()
    port = int(args.port)
    app.run(port=port)