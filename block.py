import hashlib
import random
import uuid
from Crypto.PublicKey import RSA
from transaction import Transaction

class Block:

    def __init__(self, index, timestamp, transactions, previous_hash, difficulty):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.difficulty = difficulty
        self.randomize_nonce()
        self.hash = self.hash_block()
        with open("keys/cougarcoin_private_key.pem") as f:
            self.cougarcoin_private_key = RSA.importKey(f.read())
  

    def hash_block(self):
        sha = hashlib.sha256()
        transaction_string = "".join([t.to_string() for t in self.transactions])
        material = str(self.index) + \
                   str(self.timestamp) + \
                   transaction_string + \
                   str(self.previous_hash) + \
                   str(self.nonce)
        sha.update(material.encode("utf-8"))
        return sha.hexdigest()


    def try_nonce(self):
        self.hash = self.hash_block()
        int_digest = int(self.hash,16)
        bin_string = "{0:b}".format(int_digest)
        test = bin_string[-self.difficulty:]
        check = "0" * self.difficulty
        return test == check


    def randomize_nonce(self):
        self.nonce = random.randint(0, 1000000000)


    def add_miner_transaction(self, public_key):
        prev_hash = "cougar_coin_minter_" + str(uuid.uuid4())
        transaction = Transaction(prev_hash, self.cougarcoin_private_key, public_key)
        self.transactions.append(transaction)