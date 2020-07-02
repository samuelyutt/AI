import csv, random
from node import Node

class Tree():
    def __init__(self, train_data, target_attr, selected_attrs, total_value_limit = 0.01):
        self.root = Node(train_data, target_attr, selected_attrs, 0, total_value_limit)

    def predict(self, test_data_item):
        return self.root.visit(test_data_item)


if __name__ == '__main__':
    dataset_name = 'iris'

    datasets = {'iris':         {'target_attr': 4, 'valid_attrs': [i for i in range(0, 4)]}, 
                'wdbc':         {'target_attr': 1, 'valid_attrs': [i for i in range(2, 32)]},
                'glass':        {'target_attr': 10, 'valid_attrs': [i for i in range(1, 10)]},
                'ionosphere':   {'target_attr': 34, 'valid_attrs': [i for i in range(0, 34)]},
               }

    dataset = datasets[dataset_name]
    target_attr = dataset['target_attr']
    valid_attrs = dataset['valid_attrs']
    selected_attrs = valid_attrs
    test_data_proportion = 0.3
    total_value_limit = 0.01

    data = []
    data_path = 'datasets/' + dataset_name + '.data'
    with open(data_path, newline = '') as csvfile:
        file_rows = list(csv.reader(csvfile))
        
        for file_row in file_rows:
            if not file_row:
                continue
            row = []
            for i in range(len(file_row)):
                if i == target_attr or i not in valid_attrs:
                    row.append(file_row[i])
                else:
                    row.append(float(file_row[i]))
            data.append(row)
    
    random.shuffle(data)

    train_data_count = int(len(data) * (1-test_data_proportion))
    train_data = data[:train_data_count]
    test_data = data[train_data_count:]

    tree = Tree(train_data, target_attr, selected_attrs, total_value_limit)
    
    correct_count = 0
    for td in test_data:
        prediction = tree.predict(td)
        answer = td[target_attr]
        print(prediction, answer, prediction == answer)
        if prediction == answer:
            correct_count += 1
    print(correct_count/len(test_data))
