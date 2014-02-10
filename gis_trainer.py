#!/usr/bin/env python
from trainer import Trainer
import math

class GISTrainer(Trainer):
    def __init__(self):
        self.error_threshold = 0.000001
        self.empirical_expectations = []    # E(p)
        self.model_expectations = []        # E(q)
        self.correct_constant = 0           # C
        self.condition_probabilities = []   # q(y|x)
        self.marginal_probabilities = []    # Z(x)
        self.feature_id_map = {}
        self.context_id_map = {}
        self.sum_count = 0                  # N
        self.context_counts = []            # Count(x)
        self.log_likelihood = None

    def Train(self, instances, model, iterations, model_name):
        self.__InitFromModel(model)
        self.__ComputeCorrectionConstant(instances)
        self.__ComputeEmpiricalExpectation(model)
        parameters = [0] * model.feature_size
        for i in range(iterations):
            self.__ComputeModelExpectation(model)
            if self.log_likelihood == None:
                self.log_likelihood = self.__ComputeLogLikelihood(model)
            self.__UpdateParameters(model)
            new_log_likelihood = self.__ComputeLogLikelihood(model)
            if self.__IsConverged(new_log_likelihood):
                break
            self.log_likelihood = new_log_likelihood
        model.Save(model_name)

    def __InitFromModel(self, model):
        feature_id = 0
        context_id = 0
        # Generate |feature_id| and |context_id|.
        print model.feature_map
        for feature in model.feature_map:
            self.feature_id_map[feature] = feature_id
            feature_id += 1
            if feature.context not in self.context_id_map:
                self.context_id_map[feature.context] = context_id
                context_id += 1
        # Compute |sum_count| and |context_counts|.
        self.context_counts = [0] * context_id
        for feature in model.feature_map:
            context_id = self.context_id_map[feature.context]
            feature_list = model.feature_map[feature]
            self.sum_count += len(feature_list)
            self.context_counts[context_id] += len(feature_list)

    def __ComputeEmpiricalExpectation(self, model):
        # Ep(f_i) = \sum_{x,y} p(x,y) * f_i(x,y)
        expectations = [0] * model.feature_size
        for feature in model.feature_map:
            feature_list = model.feature_map[feature]
            expectation = 0
            for feature2 in feature_list:
                expectation += 1.0 / self.sum_count * feature2.value
            feature_id = self.feature_id_map[feature]
            expectations[feature_id] = expectation
        self.empirical_expectations = expectations

    def __ComputeConditionProbability(self, model):
        # q(y|x) = 1 / Z(x) * exp( \sum_i (lambda_i * f_i(x,y) ) )
        # Z(x) = \sum_y exp( \sum_i (lambda_i * f_i(x,y)) )
        self.condition_probabilities = [0] * model.feature_size
        self.marginal_probabilities = [0] * len(model.contexts)
        for feature in model.feature_map:
            feature_id = self.feature_id_map[feature]
            feature_list = model.feature_map[feature]
            temp = 0
            parameter = model.parameters[feature_id]
            for feature2 in feature_list:
                temp += parameter * feature2.value
            temp = math.exp(temp)
            self.condition_probabilities[feature_id] = temp
            context_id = self.context_id_map[feature.context]
            self.marginal_probabilities[context_id] += temp

        for feature in model.feature_map:
            feature_id = self.feature_id_map[feature]
            context_id = self.context_id_map[feature.context]
            self.condition_probabilities[feature_id] /= \
                    self.marginal_probabilities[context_id]

    def __ComputeModelExpectation(self, model):
        # Eq(f_i) = \sum_{x,y} q(y|x) * p(x) * f_i(x, y)
        self.__ComputeConditionProbability(model)
        self.model_expectations = [0] * model.feature_size
        for feature in model.feature_map:
            feature_id = self.feature_id_map[feature]
            context_id = self.context_id_map[feature.context]
            feature_list = model.feature_map[feature]
            for feature2 in feature_list:
                print context_id, self.context_counts
                print 'feature_id:', feature_id, self.condition_probabilities, self.model_expectations
                self.model_expectations[feature_id] += \
                        self.condition_probabilities[feature_id] * \
                        self.context_counts[context_id] * feature.value

    def __ComputeCorrectionConstant(self, instances):
        # C = max sum_{x,y} f_i(x, y)
        self.correct_constant = -1
        for instance in instances:
            sum_value = 0
            for feature in instance.features:
                sum_value += feature.value
            if sum_value > self.correct_constant:
                self.correct_constant = sum_value

    def __UpdateParameters(self, model):
        parameters = [0] * model.feature_size
        for feature in model.feature_map:
            feature_id = self.feature_id_map[feature]
            parameters[feature_id] = \
                    model.parameters[feature_id] + \
                    1.0 / self.correct_constant * \
                    math.log(self.empirical_expectations[feature_id] / \
                            self.model_expectations[feature_id])
        model.parameters = parameters

    def __ComputeLogLikelihood(self, model):
        # L(p) = \sum_{x,y} p(x,y) * log( q(y|x) )
        log_likelihood = 0
        for feature in model.feature_map:
            feature_list = model.feature_map[feature]
            feature_id = self.feature_id_map[feature]
            log_likelihood += 1.0 * len(feature_list) / self.sum_count * \
                    math.log(self.condition_probabilities[feature_id])
        return log_likelihood

    def __IsConverged(self, new_log_likelihood):
        if abs(new_log_likelihood - self.log_likelihood) < self.error_threshold:
            return True
        return False