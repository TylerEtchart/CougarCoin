from miner import Miner, resolve_pseudonym
from transaction import Transaction
from serializer import Serializer
import requests
import argparse
from wallet import Wallet
from Crypto.PublicKey import RSA

class Client():

    def __init__(self, public_key, private_key):
        # save inputs
        self.private_key = private_key
        self.public_key = public_key
        self.public_key_string = public_key.exportKey().decode("utf-8")

        # build wallet
        self.wallet = Wallet(self.public_key_string)

        # register miner
        pseudonym = resolve_pseudonym(self.public_key_string)
        if pseudonym == "":
            pseudonym = input("\nChoose a pseudonym: ")
        else:
            print("\nThis key has already been registered.\nRegistered pseudonym: " + pseudonym)
        self.miner = Miner(pseudonym, self.public_key_string)
        self.s = Serializer()

        # build menu
        self.menu = "\nchoose an number:"
        self.menu += "\n1.) mine"
        self.menu += "\n2.) check balance"
        self.menu += "\n3.) make transaction"
        self.menu += "\nchoice: "


    def mine(self):
        self.miner.mine_block()
        print("\n=======================")
        print("Mined block")
        print("=======================")


    def check_balance(self):
        self.wallet.update(self.collect_transactions())
        print("\n=======================")
        print("Balance: {}".format(self.wallet.get_amount()))
        print("=======================")


    def collect_transactions(self):
        data = {
            "public_key": self.public_key_string,
        }
        r = requests.post("http://localhost:5000/collect_transactions", data=data)
        if r.text == "":
            raise ValueError("Collect transactions failed")
        else:
            return self.s.deserialize(r.text)


    def make_transaction(self):
        # ask amount
        self.wallet.update(self.collect_transactions())
        amount = input("\nHow much would you like to pay? ")
        try:
            amount = int(amount)
        except:
            print("That's not a number...")
            return
        if self.wallet.get_amount() < amount:
            print("You don't have that much money...")
            return
        elif amount < 1:
            print("The amount has to be greater than 1...")
            return

        # resolve the pseudonym
        to = input("Who would you like to pay? ")
        to_public_key = self.resolve_pseudonym(to)
        if to_public_key == "":
            print(to + " is not yet registered to the blockchain")
            return

        # make transactions
        owned_transactions = self.wallet.remove_transactions(amount)
        new_transactions = []
        for t in owned_transactions:
            new_transactions.append(Transaction(t.get_signed_transaction(), self.private_key, to_public_key))

        transaction = self.s.serialize(new_transactions)
        r = requests.post("http://localhost:5000/make_transaction", data={"transaction": transaction})
        if r.text == "":
            raise ValueError("Transaction failed")
        print("\n=======================")
        print("Make transaction")
        print("=======================")


    def main(self):
        while True:
            option = input(self.menu)
            if option == "1":
                self.mine()
            elif option == "2":
                self.check_balance()
            elif option == "3":
                self.make_transaction()
            else:
                print("Sorry, {} is not an option...".format(option))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', default="private_key1", help='The name of the key.pem')
    args = parser.parse_args()
    key = args.key
    with open("keys/" + key + ".pem") as f:
        private_key = RSA.importKey(f.read())
        public_key = private_key.publickey()

    client = Client(public_key, private_key)
    client.main()