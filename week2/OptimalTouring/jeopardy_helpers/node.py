class Node:
	def __init__(self, x, y, visit, profit, index):
		self.x = x
		self.y = y
		self.visit = visit
		self.profit = profit
		self.hours = []
		self.reach = -1
		self.wait = -1
		self.maxShift = -1
		self.path = -1
		self.index = index

