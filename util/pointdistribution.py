class PointDistribution(object):
    def __init__(self, attributes, total_points, initial_value, max_value, cost_calculator):
        self.attributes = attributes
        self.total_points = total_points
        self.used_points = 0
        self.initial_value = initial_value
        self.max_value = max_value
        self.cost_calculator = cost_calculator
        self.assigned_points = {attribute: initial_value for attribute in attributes}

    def get_value(self, attribute):
        return self.assigned_points[attribute]

    def calculate_cost(self, value):
        return self.cost_calculator(value)

    def increase_value(self, attribute):
        point_cost = self.cost_calculator(self.assigned_points[attribute])

        if ((self.total_points - (self.used_points + point_cost) >= 0)
                and self.assigned_points[attribute] < self.max_value):
            self.used_points += point_cost
            self.assigned_points[attribute] += 1

    def decrease_value(self, attribute):
        point_cost = self.cost_calculator(self.assigned_points[attribute])

        if self.assigned_points[attribute] > self.initial_value:
            self.used_points -= point_cost
            self.assigned_points[attribute] -= 1
