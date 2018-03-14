from copy import deepcopy as copy

class TransactionManager:

    def __init__(self):
        self.working_transactions = []
        self.block_transactions = []

    def add_transaction(self, transaction):
        self.working_transactions.append(transaction)

    def dump_transactions(self):
        self.block_transactions = copy(self.working_transactions)
        self.working_transactions = []

    def get_transactions(self):
        return self.block_transactions