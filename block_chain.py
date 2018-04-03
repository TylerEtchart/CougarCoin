from block import Block
from wallet import Wallet

class BlockChain:

    def __init__(self):
        self.working_chain = []
        self.indexed_blocks = {}
        self.valid_chain = {}
        self.working_block = None
        self.difficulty = 5 # Hard-coded for now...
        self.pseudonyms = {}
        self.global_wallet = {}
        self.transaction_index = {}

    def add_block(self, block):
        # add to the working chain
        self.working_chain.append(block)

        # index the block
        self.indexed_blocks[block.hash] = block
        self.working_block = None

        # add the valid blocks according to a threshold
        valid_link_threshold = 6
        if valid_link_threshold >= len(self.working_chain):
            return None
        else:
            valid_block = block
            for v in range(valid_link_threshold):
                valid_block = self.indexed_blocks[valid_block.previous_hash]
            self.valid_chain[valid_block.hash] = valid_block

            # add transactions to indices
            self.add_transactions_to_index(valid_block)
            self.add_transactions_to_global_wallet(valid_block)
            return valid_block


    # ---------------------------------------------------------

    def add_transactions_to_global_wallet(self, valid_block):
        for t in valid_block.transactions:
            signed_transaction = t.get_signed_transaction()
            prev_hash = t.get_prev_hash()
            new_owner = t.get_owner_public_key()
            self.create_wallet(new_owner)

            if prev_hash in self.global_wallet.keys():
                old_owner = self.global_wallet[prev_hash]
                self.global_wallet[old_owner].remove(prev_hash)
            
            self.global_wallet[signed_transaction] = new_owner
            self.global_wallet[new_owner].add(signed_transaction)


    def add_transactions_to_index(self, valid_block):
        for t in valid_block.transactions:
            current_hash = t.get_signed_transaction()
            prev_hash = t.get_prev_hash()
            if prev_hash in self.transaction_index.keys():
                del self.transaction_index[prev_hash]
            self.transaction_index[current_hash] = t


    # ---------------------------------------------------------
        
    def set_working_block(self, block):
        self.working_block = block

    def get_working_block(self):
        return self.working_block

    def get_difficulty(self):
        return self.difficulty

    def get_valid_transactions(self, public_key):
        if public_key in self.global_wallet.keys():
            valid_transactions = []
            for h in self.global_wallet[public_key]:
                valid_transactions.append(self.transaction_index[h])
            return valid_transactions
        else:
            return []

    def create_wallet(self, public_key):
        if public_key not in self.global_wallet.keys():
            self.global_wallet[public_key] = set([])

    def add_pseudonym(self, pseudonym, public_key):
        self.pseudonyms[public_key] = pseudonym
        self.pseudonyms[pseudonym] = public_key

    def resolve_pseudonym(self, pseudonym):
        print(self.pseudonyms)
        if pseudonym in self.pseudonyms.keys():
            temp = self.pseudonyms[pseudonym]
            print(temp)
            return temp
        else:
            return ""

    def to_html(self):
        ret = "<h1>Working Chain</h1><p>"
        for b in self.working_chain:
            verify = "{0:b}".format(int(b.hash,16))[-b.difficulty:]
            ret += "index: {}, hash: {}, prev_hash: {}, ".format(b.index, b.hash, b.previous_hash)
            ret += "block_difficulty: {}, verify: {} <br /> Transactions: <br />".format(b.difficulty, verify)
            for t in b.transactions:
                ret += t.to_string() + "<br />"
            ret += "<br />"
        ret += "</p>"

        ret += "<h1>Valid Transactions</h1><p>"
        for h, b in self.valid_chain.items():
            for t in b.transactions:
                ret += "id: {}, hash: {}, pseudonym: {}, ".format(b.index, b.hash, self.pseudonyms[t.get_owner_public_key()])
                ret += t.to_string() + "<br />"
        ret += "</p>"
        return ret