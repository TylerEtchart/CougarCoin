from miner import Miner 

def main():
    miner = None

    while True:
        if not miner:
            name = input('Miner name? ')
            miner = Miner(name) 

        option = input('\nchoose an number:\n1.) mine\n2.) check balance\nchoice: ')

        if option == "1":
            miner.mine_block()
        elif option == "2":
            wallet = miner.get_wallet()
            print("\n=======================")
            print("Balance: {}".format(wallet.amount))
            print("=======================")
        else:
            print("Sorry, {} is not an option...".format(option))


if __name__ == "__main__":
    main()