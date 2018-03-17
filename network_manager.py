from flask import Flask, abort, request
from threading import Lock
from timeit import default_timer as timer

from block import Block
from block_chain import BlockChain
from serializer import Serializer
from transaction_manager import TransactionManager
from wallet import Wallet

# flask init
app = Flask(__name__)
app.secret_key = 'super secret key'

# objects init
mutex = Lock()
s = Serializer()
block_chain = BlockChain()
transaction_manager = TransactionManager()
global_wallet = {}

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


@app.route('/get_wallet', methods=['POST']) 
def get_wallet():
    if "public_key" not in request.form:
        return ""
    else:
        return s.serialize(global_wallet[request.form["public_key"]])


@app.route('/register_miner', methods=['POST']) 
def register_miner():
    if "public_key" not in request.form:
        return 'Send the right parameters: "public_key"'
    else:
        public_key = request.form["public_key"]
        global_wallet[public_key] = Wallet(public_key)
        return ""


@app.route('/post_block', methods=['POST']) 
def post_block():
    if "block" not in request.form:
        return 'Send the right parameters: "block"'
    else:
        block_string = request.form["block"]
        block = s.deserialize(block_string)

        if block.try_nonce():
            mutex.acquire()

            # Make transactions happen in the global wallet
            valid_block = block_chain.add_block(block)
            if valid_block:
                for t in valid_block.transactions:
                    if t.from_id not in global_wallet.keys():
                        global_wallet[t.from_id] = Wallet(t.from_id)
                    if t.to_id not in global_wallet.keys():
                        global_wallet[t.to_id] = Wallet(t.to_id)
                    global_wallet[t.from_id].add_negative_transaction(t, valid_block.hash)
                    global_wallet[t.to_id].add_positive_transaction(t, valid_block.hash)

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
    app.run(port=5000)