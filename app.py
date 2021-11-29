import config
from web3 import Web3
from flask import Flask, render_template

w3 = Web3(Web3.HTTPProvider(config.INFURA_URL))
app = Flask(__name__)

@app.route("/")
def index():
    return "EthInfo!"

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