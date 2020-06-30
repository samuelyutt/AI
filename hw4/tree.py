import csv, random
from node import Node

class Tree():
    def __init__(self, train_data, target_attr, total_value_limit = 0.02):
        self.root = Node(train_data, target_attr, total_value_limit)

    def predict(self, test_data_item):
        return self.root.take_action(test_data_item)


if __name__ == '__main__':
    target_attr = 4
    test_data_proportion = 0.3
    total_value_limit = 0.02

    data = []
    with open('datasets/iris/iris.data', newline = '') as csvfile:
        file_rows = list(csv.reader(csvfile))
        
        for file_row in file_rows:
            if not file_row:
                continue
            row = []
            for i in range(len(file_row)):
                if i == target_attr:
                    row.append(file_row[i])
                else:
                    row.append(float(file_row[i]))
            data.append(row)
    
    random.shuffle(data)

    train_data_count = int(len(data) * (1-test_data_proportion))
    train_data = data[:train_data_count]
    test_data = data[train_data_count:]

    t = Tree(train_data, target_attr, total_value_limit)
    
    correct_count = 0
    for td in test_data:
        prediction = t.predict(td)
        answer = td[target_attr]
        print(prediction, answer, prediction == answer )
        if prediction == answer:
            correct_count += 1
    print(correct_count/len(test_data))
