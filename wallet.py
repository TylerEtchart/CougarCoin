class Wallet:

    def __init__(self, public_key):
        self.public_key = public_key
        self.transactions = {}


    def add_transactions(self, transactions):
        for t in transactions:
            self.transactions[t.get_signed_transaction()] = t


    def remove_transactions(self, amount):
        removed_transactions = []
        kept_transactions = {}
        added = 0
        for h, t in self.transactions.items():
            if added < amount:
                removed_transactions.append(t)
                added += 1
            else:
                kept_transactions[h] = t

        self.transactions = kept_transactions
        return removed_transactions


    def update(self, transactions):
        self.transactions = {}
        for t in transactions:
            self.transactions[t.get_signed_transaction()] = t


    def get_amount(self):
        return len(self.transactions)