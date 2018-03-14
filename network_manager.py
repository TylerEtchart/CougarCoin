from flask import Flask, abort, request
from threading import Lock
from timeit import default_timer as timer

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
    transaction_manager.add_transaction("Got block") # add a dummy transaction
    return s.serialize(block_chain.get_working_block())


@app.route('/post_block', methods=['POST']) 
def post_block():
    if "block" not in request.form:
        return 'Send the right parameters: "block" and "nonce"'
    else:
        block_string = request.form["block"]
        block = s.deserialize(block_string)

        if block.try_nonce():
            mutex.acquire()
            transaction_manager.dump_transactions()
            block_chain.add_block(block)
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