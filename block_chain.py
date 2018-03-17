from block import Block

class BlockChain:

    def __init__(self):
        self.working_chain = []
        self.indexed_blocks = {}
        self.valid_chain = {}
        self.working_block = None
        self.difficulty = 5 # Hard-coded for now...

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
            return valid_block
        
    def set_working_block(self, block):
        self.working_block = block

    def get_working_block(self):
        return self.working_block

    def get_difficulty(self):
        return self.difficulty

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
                ret += "id: {}, hash: {}, ".format(b.index, b.hash)
                ret += t.to_string() + "<br />"
        ret += "</p>"
        return ret