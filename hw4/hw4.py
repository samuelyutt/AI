import csv, random, statistics
from tree import Tree

datasets = {'iris':         {'target_attr': 4, 'valid_attrs': [i for i in range(0, 4)]}, 
            'wdbc':         {'target_attr': 1, 'valid_attrs': [i for i in range(2, 32)]},
            'glass':        {'target_attr': 10, 'valid_attrs': [i for i in range(1, 10)]},
            'ionosphere':   {'target_attr': 34, 'valid_attrs': [i for i in range(0, 34)]},
            'wine':         {'target_attr': 0, 'valid_attrs': [i for i in range(1, 14)]},
            }

def data_reader(dataset_name):
    dataset = datasets[dataset_name]
    target_attr = dataset['target_attr']
    valid_attrs = dataset['valid_attrs']

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
    return data, target_attr, valid_attrs


def data_processor(data, test_data_proportion):
    random.shuffle(data)
    train_data_count = int(len(data) * (1-test_data_proportion))
    train_data = data[:train_data_count]
    test_data = data[train_data_count:]
    return train_data, test_data


def build_forest(tree_count, selected_attrs_count, train_data, target_attr, valid_attrs, total_value_limit, print_mode=False):
    forest = []

    for _ in range(tree_count):
        selected_attrs = random.sample(valid_attrs, selected_attrs_count)
        if print_mode:
            print('Building Tree', _+1, selected_attrs)
        forest.append( Tree(train_data, target_attr, selected_attrs, total_value_limit) )

    return forest


def test(test_data, target_attr, forest, print_mode=False):
    if print_mode:
        print('Testing')
    correct_count = 0
    
    for td in test_data:
        votes = {}

        for tree in forest:
            prediction = tree.predict(td)
            if prediction in votes:
                votes[ prediction ] += 1
            else:
                votes[ prediction ] = 1
        # print(votes)
        
        final_decision = None
        max_vote = -1
        for prediction in votes:
            if votes[ prediction ] > max_vote:
                final_decision = prediction
                max_vote = votes[ prediction ]

        answer = td[target_attr]
        if print_mode:
            print(final_decision == answer, final_decision, answer, votes)
        if final_decision == answer:
            correct_count += 1
    
    if print_mode:
        print(correct_count/len(test_data))

    return correct_count / len(test_data)


def simple_test(tree_count, selected_attrs_count, train_data, test_data, target_attr, valid_attrs, total_value_limit=0.01, print_mode=False):
    forest = build_forest(tree_count, selected_attrs_count, train_data, target_attr, valid_attrs, total_value_limit, False)
    accuracy = test(test_data, target_attr, forest, False)
    if print_mode:
        print('{}\t{}\t{}\t{}'.format(tree_count, selected_attrs_count, total_value_limit, accuracy))
    return accuracy


def example_test():
    dataset_name = 'wine'
    test_data_proportion = 0.3
    total_value_limit = 0.01

    dataset, target_attr, valid_attrs = data_reader(dataset_name)
    train_data, test_data = data_processor(dataset, test_data_proportion)
    
    print('==== Example Test ====')
    print('Dataset:\t', dataset_name)
    print()
    print('Trees\tAttrs\tLimit\tAccuracy')
    simple_test(10, 7, train_data, test_data, target_attr, valid_attrs, total_value_limit, True)


def datasets_test(test_count=10):
    test_datasets = ['iris', 'wdbc', 'glass', 'ionosphere', 'wine']
    test_data_proportion = 0.3
    total_value_limit = 0.01

    print()
    print('==== Datasets Test ====')
    print('test_count:\t\t', test_count)
    print('test_data_proportion:\t', test_data_proportion)
    print('total_value_limit:\t', total_value_limit)
    print('trees_count:\t\t', 1)
    print()
    print('Dataset\tAccuracy')
    
    for dataset_name in test_datasets:
        dataset, target_attr, valid_attrs = data_reader(dataset_name)

        accuracies = []
        for _ in range(test_count):
            train_data, test_data = data_processor(dataset, test_data_proportion)
            accuracy = simple_test(1, len(valid_attrs), train_data, test_data, target_attr, valid_attrs, total_value_limit)
            accuracies.append(accuracy)
        print('{}\t{}'.format(dataset_name, statistics.mean(accuracies)))


def trees_count_test(dataset_name, max_trees_count, selected_attrs_count=None, test_count=10):
    test_data_proportion = 0.3
    total_value_limit = 0.01

    dataset, target_attr, valid_attrs = data_reader(dataset_name)
    train_data, test_data = data_processor(dataset, test_data_proportion)
    selected_attrs_count = selected_attrs_count if selected_attrs_count else int(len(valid_attrs)/2)

    print()
    print('==== Trees Count Test ====')
    print('Dataset:\t\t', dataset_name)
    print('test_count:\t\t', test_count)
    print('test_data_proportion:\t', test_data_proportion)
    print('total_value_limit:\t', total_value_limit)
    print('selected_attrs_count:\t', selected_attrs_count)
    print()
    print('Trees\tAccuracy')

    for trees_count in range(1, max_trees_count+1):
        accuracies = []
        for _ in range(test_count):
            accuracy = simple_test(trees_count, selected_attrs_count, train_data, test_data, target_attr, valid_attrs, total_value_limit)
            accuracies.append(accuracy)
        print('{}\t{}'.format(trees_count, statistics.mean(accuracies)))


def attrs_count_test(dataset_name, trees_count, test_count=10):
    test_data_proportion = 0.3
    total_value_limit = 0.01

    dataset, target_attr, valid_attrs = data_reader(dataset_name)
    train_data, test_data = data_processor(dataset, test_data_proportion)

    print()
    print('==== Attrs Count Test ====')
    print('Dataset:\t\t', dataset_name)
    print('test_count:\t\t', test_count)
    print('test_data_proportion:\t', test_data_proportion)
    print('total_value_limit:\t', total_value_limit)
    print('trees_count:\t\t', trees_count)
    print()
    print('Attrs\tAccuracy')

    for selected_attrs_count in range(1, len(valid_attrs)+1):
        accuracies = []
        for _ in range(test_count):
            accuracy = simple_test(trees_count, selected_attrs_count, train_data, test_data, target_attr, valid_attrs, total_value_limit)
            accuracies.append(accuracy)
        print('{}\t{}'.format(selected_attrs_count, statistics.mean(accuracies)))


def test_data_propotion_test(dataset_name, trees_count, selected_attrs_count=None, test_count=10):
    total_value_limit = 0.01

    dataset, target_attr, valid_attrs = data_reader(dataset_name)
    selected_attrs_count = selected_attrs_count if selected_attrs_count else int(len(valid_attrs)/2)

    print()
    print('==== Test Data Propotion Test ====')
    print('Dataset:\t\t', dataset_name)
    print('test_count:\t\t', test_count)
    print('total_value_limit:\t', total_value_limit)
    print('trees_count:\t\t', trees_count)
    print('selected_attrs_count:\t', selected_attrs_count)
    print()
    print('test/all\tAccuracy')

    for i in range(1, 10):
        test_data_proportion = i / 10
        train_data, test_data = data_processor(dataset, test_data_proportion)

        accuracies = []
        for _ in range(test_count):
            accuracy = simple_test(trees_count, selected_attrs_count, train_data, test_data, target_attr, valid_attrs, total_value_limit)
            accuracies.append(accuracy)
        print('{}\t{}'.format(test_data_proportion, statistics.mean(accuracies)))

def total_value_limit_test(dataset_name, trees_count, selected_attrs_count=None, test_count=10):
    total_value_limits = [1.0, 0.5, 0.1, 0.05, 0.01, 0.005, 0.0001]
    test_data_proportion = 0.3

    dataset, target_attr, valid_attrs = data_reader(dataset_name)
    train_data, test_data = data_processor(dataset, test_data_proportion)
    selected_attrs_count = selected_attrs_count if selected_attrs_count else int(len(valid_attrs)/2)

    print()
    print('==== Total Value Limit Test ====')
    print('Dataset:\t\t', dataset_name)
    print('test_count:\t\t', test_count)
    print('test_data_proportion:\t', test_data_proportion)
    print('trees_count:\t\t', trees_count)
    print('selected_attrs_count:\t', selected_attrs_count)
    print()
    print('Limit\tAccuracy')

    for total_value_limit in total_value_limits:
        accuracies = []
        for _ in range(test_count):
            accuracy = simple_test(trees_count, selected_attrs_count, train_data, test_data, target_attr, valid_attrs, total_value_limit)
            accuracies.append(accuracy)
        print('{}\t{}'.format(total_value_limit, statistics.mean(accuracies)))



def main():
    example_test()
    print('\n++++++++++++++++++++++++++++\n')
    
    datasets_test()
    print('\n++++++++++++++++++++++++++++\n')

    test_datasets = ['iris', 'wdbc', 'glass', 'ionosphere', 'wine']
    
    for dataset in test_datasets:
        trees_count_test(dataset, 30)
        print()
    print('\n++++++++++++++++++++++++++++\n')


    for dataset in test_datasets:
        attrs_count_test(dataset, 10)
        print()
    print('\n++++++++++++++++++++++++++++\n')
    
    for dataset in test_datasets:
        test_data_propotion_test(dataset, 10)
        print()
    print('\n++++++++++++++++++++++++++++\n')
    
    for dataset in test_datasets:
        total_value_limit_test(dataset, 10)
        print()
    print('\n++++++++++++++++++++++++++++\n')




if __name__ == '__main__':
    main()