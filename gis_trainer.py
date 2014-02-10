#!/usr/bin/env python
from trainer import Trainer

class GISTrainer(Trainer):
    def __init__(self):
        self.empirical_expectations = []
        self.model_expectations = []
        self.correct_constant = 0
        self.condition_probabilities = []
        self.marginal_probabilities = []
        self.feature_id_map = {}

    def Train(self, instances, model):
        __ComputeCorrectionConstant(instances)
        __ComputeEmpiricalExpectation(model)
        __ComputeModelExpectation(model)

    def __ComputeEmpiricalExpectation(self, model):
        # Ep(f_i) = \sum_{x,y} p(x,y) * f_i(x,y)
        expectations = []
        feature_id = 0
        for feature in model.feature_map:
            feature_id_map[feature] = feature_id
            feature_id += 1
            feature_list = model.feature_map[feature]
            expectation = 0
            sum_count = len(feature_list)
            for feature2 in feature_list:
                expectation += 1.0 / sum_count * feature2.value
            expectations.append(expectation)
        self.empirical_expectations = expectations

    def __ComputeConditionProbability(self, model):
        # q(y|x) = 1 / Z(x) * exp( \sum_i (lambda_i * f_i(x,y) ) )
        # Z(x) = \sum_y exp( \sum_i (lambda_i * f_i(x,y)) )
        self.condition_probabilities = [0] * model.feature_size
        for feature in model.feature_map:
            feature_id = feature_id_map[feature]
            feature_list = model.feature_map[feature]
            temp = 0
            parameter = model.parameters[feature_id]
            for feature2 in feature_list:
                temp += parameter * feature2.value
            self.condition_probabilities[feature_id] = exp(temp)
        self.marginal_probabilities = [0] * len(model.contexts)
        for context in model.contexts:
            probability = 0
            for label in model.labels:
                feature = Feature(context, label, 0)
                if feature in model.feature_map:
                    feature_id = feature_id_map[feature]
                    parameter = model.parameters[feature_id]
                    feature_list = model.feature_map[feature]
                    temp = 0
                    for feature2 in feature_list:
                        temp += parameter * feature2.value
                    probability += exp(temp)
            #self.marginal_probabilities[]

        #marginal_probabilities = 

    def __ComputeModelExpectation(self, model):
        # Eq(f_i) = \sum_{x,y} q(y|x) * p(x) * f_i(x, y)
        pass

    def __ComputeCorrectionConstant(self, instances):
        # C = max sum_{x,y} f_i(x, y)
        self.correct_constant = -1
        for instance in instances:
            sum_value = 0
            for feature in instance.features:
                sum_value += feature.value
            if sum_value > self.correct_constant:
                self.correct_constant = sum_value



