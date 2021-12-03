import config
import ccxt
import time
from web3 import Web3
from flask import Flask, render_template
import json

w3 = Web3(Web3.HTTPProvider(config.INFURA_URL))
app = Flask(__name__)

with open('miners.json') as f:
    miners = json.load(f)    

def sec_to_time_qty(secs):
    s_per_d = 86400
    s_per_h = 3600
    s_per_m = 60

    days = secs // s_per_d
    secs = secs % s_per_d
    hours = secs // s_per_h
    secs = secs % s_per_h
    minutes = secs // s_per_m
    seconds = round(secs % s_per_m)
    
    return days, hours, minutes, seconds

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

    return render_template("index.html", 
                            eth_price=eth_price,
                            latest_blocks=latest_blocks,
                            latest_transactions=latest_transactions,
                            miners=miners)


@app.route("/tx/<tx_hash>")
def transaction(tx_hash):
    tx = w3.eth.get_transaction(tx_hash)
    return render_template("transaction.html", tx_hash=tx_hash, tx=tx)


@app.route("/address/<address_hash>")
def address(address_hash):
    balance = w3.eth.getBalance(address_hash)
    balance_in_eth = float(Web3.fromWei(balance, 'ether'))

    binance = ccxt.binance() 
    eth_price = (binance.fetch_ticker('ETH/USDC'))['last']
    total_usd_value = round((balance_in_eth * eth_price), 2)

    transaction_count = w3.eth.get_transaction_count(address_hash)

    return render_template("address.html", address_hash=address_hash,
                            balance_in_eth=balance_in_eth,
                            total_usd_value=total_usd_value,
                            eth_price=eth_price,
                            transaction_count=transaction_count)


@app.route("/block/<block_num>")
def block(block_num):
    block = w3.eth.get_block(int(block_num))
    current_time = time.time()
    block_time = int(block.timestamp)
    block_time_str = time.ctime(block_time)
    time_diff = current_time - block_time
    days, hours, minutes, seconds = sec_to_time_qty(time_diff)

    return render_template("block.html", block=block,
                            days=days,
                            hours=hours,
                            minutes=minutes,
                            seconds=seconds,
                            block_time_str=block_time_str)