from block import Block

class BlockChain:

    def __init__(self):
        self.chain = []
        self.working_block = None
        self.difficulty = 3 # Hard-coded for now...

    def add_block(self, block):
        self.chain.append(block)
        self.working_block = None
        
    def set_working_block(self, block):
        self.working_block = block

    def get_working_block(self):
        return self.working_block

    def get_difficulty(self):
        return self.difficulty

    def to_html(self):
        ret = "<p>"
        for b in self.chain:
            verify = "{0:b}".format(int(b.hash,16))[-b.difficulty:]
            ret += "index: {}, hash: {}, prev_hash: {}, ".format(b.index, b.hash, b.previous_hash)
            ret += "block_difficulty: {}, verify: {} <br /> Transactions: <br />".format(b.difficulty, verify)
            for t in b.transactions:
                ret += t + "<br />"
            ret += "<br />"
        ret += "</p>"
        return ret