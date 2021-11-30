import config
import ccxt
import time
from web3 import Web3
from flask import Flask, render_template

w3 = Web3(Web3.HTTPProvider(config.INFURA_URL))
app = Flask(__name__)

@app.route("/")
def index():
    binance = ccxt.binance() 
    eth_price = binance.fetch_ticker('ETH/USDC')
    latest_block = w3.eth.get_block('latest')

    latest_blocks = []
    for block_number in range(latest_block.number, latest_block.number-10, -1):
        block = w3.eth.get_block(block_number)
        latest_blocks.append(block)

    latest_transactions = []
    for tx in latest_blocks[-1]['transactions'][-10:]:
        transaction = w3.eth.get_transaction(tx)
        latest_transactions.append(transaction)

    current_time = time.time()

    return render_template("index.html", 
                            eth_price=eth_price,
                            latest_blocks=latest_blocks,
                            latest_transactions=latest_transactions,
                            current_time=current_time)

@app.route("/tx/<tx_hash>")
def transaction(tx_hash):
    tx = w3.eth.get_transaction(tx_hash)
    return render_template("transaction.html", tx_hash=tx_hash, tx=tx)


@app.route("/address/<address_hash>")
def address(address_hash):
    return render_template("address.html", address_hash=address_hash)


@app.route("/block/<block_hash>")
def block(block_hash):
    return render_template("block.html", block_hash=block_hash)