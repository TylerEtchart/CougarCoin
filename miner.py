from timeit import default_timer as timer
from block import Block
import requests
from serializer import Serializer
import random

class Miner:

    def __init__(self, public_key):
        self.public_key = public_key
        self.serializer = Serializer()

    def get_block(self):
        r = requests.get("http://localhost:5000/get_block")
        return self.serializer.deserialize(r.text)

    def post_block(self, block):
        block_string = self.serializer.serialize(block)
        data = {
            "block": block_string,
        }
        r = requests.post("http://localhost:5000/post_block", data=data)
        if r.text != "":
            raise ValueError(r.text)
        
    def mine_block(self):
        succeded = False
        while not succeded:
            block = self.get_block()
            block.add_miner_transaction(self.public_key)
            block.randomize_nonce()
            succeded = block.try_nonce()
        self.post_block(block)

    def mine(self):
        while True:
            self.mine_block()


if __name__ == "__main__":
    miner = Miner("Miner {}".format(random.randint(0,10)))
    miner.mine()