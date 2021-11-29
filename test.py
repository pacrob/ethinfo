import config
from web3 import Web3

w3 = Web3(Web3.HTTPProvider(config.INFURA_URL))

print(w3.eth.block_number)

my_bal = w3.eth.get_balance(config.MY_MEW_WALLET)
print(w3.fromWei(my_bal, 'ether'))

trans = w3.eth.get_transaction(config.MY_LAST_TRANS)
print(trans)