from random import *
from collections import namedtuple

MIN_PERCENT = 2
MAX_PERCENT = 50
MIN_AMOUNT = 0.01
MAX_AMOUNT = 10
NUMBER_OF_DIGITS = 6

Order = namedtuple('Order', 'price, amount')

class Exchange:

	def __init__(self, initial_rate):
		self.exchange_rate = initial_rate
		self.buy_orders = []
		self.sell_orders = []
		self.deals = []

	def model_exchange_rate(self):
		global exchange_rate
		delta = 0.001 * random() * self.exchange_rate
		will_increase = choice([True, False])
		if (will_increase):
			self.exchange_rate += delta
		else:
			self.exchange_rate -= delta
		self.exchange_rate = round(self.exchange_rate, NUMBER_OF_DIGITS)

	def get_amount(self):
		return random() * (MAX_AMOUNT - MIN_AMOUNT) + MIN_AMOUNT

	def get_deviation_percent(self):
		return min([random() for i in range(7)]) * (MAX_PERCENT - MIN_PERCENT) + MIN_PERCENT

	def gen_new_buy_order(self):
		deviation_percent = self.get_deviation_percent()
		price = round(self.exchange_rate * (1 - deviation_percent * 0.01), NUMBER_OF_DIGITS)
		amount = self.get_amount()
		self.buy_orders.append(Order(price, amount))

	def gen_new_sell_order(self):
		deviation_percent = self.get_deviation_percent()
		price = round(self.exchange_rate*(1 + deviation_percent * 0.01), NUMBER_OF_DIGITS)
		amount = self.get_amount()
		self.sell_orders.append(Order(price, amount))

	def find_obsolete_buy_orders(self):
		for buy_order in self.buy_orders:
			if (buy_order.price < ((100 - MAX_PERCENT) / 100) * self.exchange_rate):
				self.buy_orders.remove(buy_order)

	def find_obsolete_sell_orders(self):
		for sell_order in self.sell_orders:
			if (sell_order.price > ((100 + MAX_PERCENT) / 100) * self.exchange_rate):
				self.sell_orders.remove(sell_order)

	def find_profitable_sell_orders(self):
		for sell_order in self.sell_orders:
			if (sell_order.price < ((100 + MIN_PERCENT) / 100) * self.exchange_rate):
				amount = sell_order.amount * random()
				self.buy_orders.append(sell_order.price, amount)
				self.buy_orders.append(sell_order, sell_order.amount - amount)

	def make_deals(self):
		self.buy_orders.sort(reverse = True)
		self.sell_orders.sort()
		while(len(self.sell_orders) != 0):
			sell_order = self.sell_orders.pop(0)
			while (len(self.buy_orders) != 0 and sell_order.amount != 0 and sell_order.price <= self.buy_orders[0].price):
				buy_order = self.buy_orders.pop(0)
				if (sell_order.amount > buy_order.amount):
					self.deals.append(buy_order)
					sell_order = Order(sell_order.price, sell_order.amount - buy_order.amount)
				else:
					self.deals.append(sell_order)
					self.buy_orders.insert(0, Order(buy_order.price, buy_order.amount - sell_order.amount))
					sell_order = Order(0, 0)
			if (sell_order.amount != 0):
				self.sell_orders.insert(0, sell_order)
				return

	def add_random_order(self):
		is_buy_order = choice([True, False])
		if (is_buy_order):
			self.gen_new_buy_order()
		else:
			self.gen_new_sell_order()

	def process_orders(self):
		self.find_obsolete_buy_orders()
		self.find_obsolete_sell_orders()
		self.find_profitable_sell_orders()
		self.make_deals()