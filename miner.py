from timeit import default_timer as timer
from block import Block
import requests
from serializer import Serializer
import random
import argparse
from Crypto.PublicKey import RSA

def resolve_pseudonym(pseudonym):
    data = {
        "pseudonym": pseudonym,
    }
    r = requests.post("http://localhost:5000/resolve_pseudonym", data=data)
    return r.text

class Miner:

    def __init__(self, pseudonym, public_key):
        self.public_key = public_key
        self.serializer = Serializer()
        data = {
            "pseudonym": pseudonym,
            "public_key": public_key,
        }
        r = requests.post("http://localhost:5000/register_miner", data=data)
        if r.text != "":
            raise ValueError(r.text)


    def get_block(self):
        r = requests.get("http://localhost:5000/get_block")
        return self.serializer.deserialize(r.text)


    def post_block(self, block):
        block_string = self.serializer.serialize(block)
        data = {
            "block": block_string
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
        print("Mining...")
        while True:
            self.mine_block()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', default="private_key1", help='The name of the key.pem')
    args = parser.parse_args()
    key = args.key
    with open("keys/" + key + ".pem") as f:
        private_key = RSA.importKey(f.read())
        public_key = private_key.publickey()
        public_key_string = public_key.exportKey().decode("utf-8")

    pseudonym = resolve_pseudonym(public_key_string)
    if pseudonym == "":
        pseudonym = input("\nChoose a pseudonym: ")
    else:
        print("\nThis key has already been registered.\nRegistered pseudonym: " + pseudonym)

    miner = Miner(pseudonym, public_key_string)
    miner.mine()