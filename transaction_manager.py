from copy import deepcopy as copy

class TransactionManager:

    def __init__(self):
        self.working_transactions = []
        self.block_transactions = []

    def add_transactions(self, transactions):
        self.working_transactions.extend(transactions)

    def dump_transactions(self):
        self.block_transactions = copy(self.working_transactions)
        self.working_transactions = []

    def get_transactions(self):
        return self.block_transactions