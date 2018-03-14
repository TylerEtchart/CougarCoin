import hashlib
import random

class Block:

    def __init__(self, index, timestamp, transactions, previous_hash, difficulty):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.difficulty = difficulty
        self.randomize_nonce()
        self.hash = self.hash_block()
  
    def hash_block(self):
        sha = hashlib.sha256()
        transaction_string = "".join(str(self.transactions))
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

    def add_miner_transaction(self, name):
        self.transactions.append(name)