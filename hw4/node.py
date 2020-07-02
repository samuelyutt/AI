class Node():
    def __init__(self, data, target_attr, selected_attrs, depth=0, total_value_limit=0.01):
        self.action = None
        self.threshold = None
        self.threshold_value = None
        self.prediction = None
        self.data = data
        self.target_attr = target_attr
        self.selected_attrs = selected_attrs
        self.lt_value_child = None
        self.ge_value_child = None
        self.depth = depth
        self.total_value_limit = total_value_limit

        total_value = self.gini_index(data=self.data)
        if total_value < total_value_limit or depth > 100:
            # print('predict')
            self.action = 'predict'
            self.prediction = self.make_prediction()
            self.data = None
        else:
            # print('split')
            self.split(total_value)

    def __str__(self):
        ret = self.action + '\n'
        ret += str(self.depth) + '\n'
        ret += str(self.prediction) + '\n'
        ret += str(self.threshold) + '\n'
        ret += str(self.threshold_value) + '\n'
        return ret

    def stats(self, data):
        stats = {}
        for row in data:
            if row[self.target_attr] in stats:
                stats[ row[self.target_attr] ] += 1
            else:
                stats[ row[self.target_attr] ] = 1
        return stats

    def make_prediction(self):
        prediction = None

        stats = self.stats(self.data)
        max_count = -1
        for target in stats:
            if stats[target] > max_count:
                prediction = target
                max_count = stats[target]

        return prediction

    def gini_index(self, data):
        data_count = len(data)
        if data_count == 0:
            return 0
        
        stats = self.stats(data)
        probabilities = []
        for target in stats:
            probabilities.append(stats[target] / data_count)

        total_power_of_probabilities = 0
        for p in probabilities:
            total_power_of_probabilities += p * p
        gini_index = 1 - total_power_of_probabilities

        return gini_index

    def remainder(self, key, value):
        lt_value_data, ge_value_data = self.split_data_by_value(key, value)
        
        remainder = (self.gini_index(data=lt_value_data) * len(lt_value_data) +
                    self.gini_index(data=ge_value_data) * len(ge_value_data)) / len(self.data)

        return remainder

    def split_data_by_value(self, key, value):
        lt_value_data = []
        ge_value_data = []
        for row in self.data:
            if row[key] < value:
                lt_value_data.append(row)
            else:
                ge_value_data.append(row)
        return lt_value_data, ge_value_data

    def select_threshold(self, total_value):
        info_gain = None
        threshold = None
        threshold_value = None

        for key in self.selected_attrs:
            values = []
            for row in self.data:
                values.append(row[key])
            values.sort()
            values.remove(values[0])

            for value in values:
                tmp_info_gain = total_value - self.remainder(key, value)
                if threshold is None or tmp_info_gain > info_gain:
                    info_gain = tmp_info_gain
                    threshold = key
                    threshold_value = value

        return threshold, threshold_value

    def split(self, total_value):
        threshold, threshold_value = self.select_threshold(total_value)
        lt_value_data, ge_value_data = self.split_data_by_value(threshold, threshold_value)
        self.data = None
        self.action = 'catagorize'
        self.threshold = threshold
        self.threshold_value = threshold_value
        self.lt_value_child = Node(lt_value_data, self.target_attr, self.selected_attrs, self.depth+1, self.total_value_limit)
        self.ge_value_child = Node(ge_value_data, self.target_attr, self.selected_attrs, self.depth+1, self.total_value_limit)

    def visit(self, test_data_item):
        if self.action == 'predict':
            return self.prediction
        else:
            if test_data_item[self.threshold] < self.threshold_value:
                return self.lt_value_child.visit(test_data_item)
            else:
                return self.ge_value_child.visit(test_data_item)

		