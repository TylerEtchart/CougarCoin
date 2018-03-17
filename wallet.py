class Wallet:

    def __init__(self, name):
        self.name = name
        self.amount = 0
        self.positve_transactions = []
        self.negative_transactions = []

    def add_negative_transaction(self, transaction, block_hash):
        self.amount -= transaction.amount
        self.negative_transactions.append((transaction, block_hash))

    def add_positive_transaction(self, transaction, block_hash):
        self.amount += transaction.amount
        self.positve_transactions.append((transaction, block_hash))