import hashlib

class Transaction:

    def __init__(self, prev_hash, from_private_key, to_public_key):
        sha = hashlib.sha256()
        material = str(prev_hash) + to_public_key
        sha.update(material.encode("utf-8"))
        hashed_material = sha.hexdigest().encode("utf-8")
        self.signed_transaction = from_private_key.sign(hashed_material, "not_used_param")[0]
        self.owner_public_key = to_public_key
        self.prev_hash = prev_hash


    def get_prev_hash(self):
        return self.prev_hash


    def get_owner_public_key(self):
        return self.owner_public_key


    def get_signed_transaction(self):
        return self.signed_transaction


    def to_string(self):
        return "prev_hash: {}, owner: {}, signed_transaction: {}".format(self.prev_hash, self.owner_public_key, self.signed_transaction)