from node import Node

class Tree():
    def __init__(self, train_data, target_attr, selected_attrs, total_value_limit = 0.01):
        self.root = Node(train_data, target_attr, selected_attrs, 0, total_value_limit)

    def predict(self, test_data_item):
        return self.root.visit(test_data_item)
