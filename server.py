from flask import Flask
from time import *
import json
import threading
import logic

exchange = logic.Exchange(10000)

#transactions_per_minute = EXPECTED_TRANSACTIONS_PER_MINUTE - real_number 

transactions_per_minute = 4

def exchange_run():
	while(True):
		for i in range (transactions_per_minute):
			exchange.add_random_order()
			sleep(1/transactions_per_minute)
		exchange.model_exchange_rate()
		exchange.process_orders()

threading.Thread(target=exchange_run).start()

app = Flask(__name__)

@app.route('/')
def hello():
	return 'hello world'

@app.route('/api/v1/exchange_rate/')
def get_rate():
	return json.dumps(exchange.exchange_rate)

@app.route('/api/v1/deals')
def get_deals():
	return json.dumps(exchange.deals[0:20])

@app.route('/api/v1/orders/buy')
def get_buy_orders():
	return json.dumps(exchange.buy_orders[0:20])

@app.route('/api/v1/orders/sell')
def get_sell_orders():
	return json.dumps(exchange.sell_orders[0:20])


