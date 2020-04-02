from board import position


class node:
	def __init__(self, parent_, position_):
		self.parent = parent_
		self.position = position_
		self.childs = []

	def add_child(self, child_node):
		self.childs.append(child_node)