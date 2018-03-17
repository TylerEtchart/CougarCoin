class Transaction:

    def __init__(self, from_id, to_id, amount):
        self.from_id = from_id
        self.to_id = to_id
        self.amount = amount

    def get_from(self):
        return self.from_id

    def get_to(self):
        return self.to_id

    def get_amount(self):
        return self.amount

    def to_string(self):
        return "from: {}, to: {}, amount: {}".format(self.from_id, self.to_id, self.amount)