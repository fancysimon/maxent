#!/usr/bin/env python
from trainer import Trainer
from feature import Feature
import math
import sys

class GISTrainer(Trainer):
    def __init__(self):
        self.error_threshold = 0.000001
        self.empirical_expectations = []    # E(p)
        self.model_expectations = []        # E(q)
        self.correct_constant = 0           # C
        self.condition_probabilities = []   # q(y|x)
        self.marginal_probabilities = []    # Z(x)
        self.sum_count = 0                  # N: instance count
        self.context_counts = []            # Count(x)
        self.log_likelihood = 99999
        self.zero = 1e-323
        self.log_zero = math.log(self.zero)

    def Train(self, instances, model, iterations):
        print 'iters   loglikelihood    training accuracy'
        print '=========================================='
        self.__InitFromModel(instances, model)
        self.__ComputeCorrectionConstant(instances)
        self.__ComputeEmpiricalExpectation(instances, model)
        parameters = [0] * model.feature_size
        for i in range(1, iterations+1):
            correct_rate, new_log_likelihood = \
                    self.__ComputeModelExpectation(instances, model)
            #print 'new_log_likelihood:', new_log_likelihood
            print '  %d\t%.6f\t %.1f%%' % (i, new_log_likelihood/self.sum_count, correct_rate * 100)
            sys.stdout.flush()
            self.__UpdateParameters(model)
            if self.__IsConverged(new_log_likelihood):
                break
            self.log_likelihood = new_log_likelihood
        print '=========================================='

    def __InitFromModel(self, instances, model):
        # Compute |sum_count| and |context_counts|.
        self.context_counts = [0] * len(model.context_id_map)
        for instance in instances:
            context_id_map = {}
            for feature in instance.features:
                context_id = model.context_id_map[feature.context]
                context_id_map[context_id] = 1
            for context_id in context_id_map:
                self.context_counts[context_id] += 1
        self.sum_count = len(instances)
        print 'Instance number:', self.sum_count
        #print 'self.context_counts:', self.context_counts

    def __ComputeEmpiricalExpectation(self, instances, model):
        # Ep(f_i) = \sum_{x,y} p(x,y) * f_i(x,y)
        expectations = [0] * model.feature_size
        for instance in instances:
            for feature in instance.features:
                context_id = model.context_id_map[feature.context]
                feature_id = model.feature_id_map[feature]
                expectations[feature_id] += 1.0 / self.sum_count * feature.value
        self.empirical_expectations = expectations
        #print 'self.empirical_expectations:', self.empirical_expectations

    def ComputeConditionProbability(self, instance, model):
        # q(y|x) = 1 / Z(x) * exp( \sum_i (lambda_i * f_i(x,y) ) )
        # Z(x) = \sum_y exp( \sum_i (lambda_i * f_i(x,y)) )
        probabilities = [0.0] * len(model.labels)
        #print 'label:', instance.label
        #print 'features:', instance.features
        for feature in instance.features:
            context = feature.context
            #context_id = model.context_id_map[context]
            
            for i in range(len(probabilities)):
                label = model.labels[i]
                feature2 = Feature(context, label, 0)
                if feature2 in model.feature_id_map:
                    feature_id = model.feature_id_map[feature2]
                    parameter = model.parameters[feature_id]
                    label_id = model.label_id_map[label]
                    probabilities[label_id] += parameter * feature.value
        #print 'probabilities:', probabilities
        
        label = model.labels[0]
        max_probability = -999999
        for i in range(len(probabilities)):
            if probabilities[i] > max_probability:
                label = model.labels[i]
                max_probability = probabilities[i]
        # Normalize.
        for i in range(len(probabilities)):
            probabilities[i] = math.exp(probabilities[i] - max_probability)
        
        self.condition_probabilities = [0.0] * len(model.labels)
        
        sum_probability = sum(probabilities)
        for i in range(len(probabilities)):
            probabilities[i] = float(probabilities[i]) / sum_probability
        #print 'condition_probabilities:', probabilities
        return label, probabilities

    def __ComputeModelExpectation(self, instances, model):
        # Eq(f_i) = \sum_{x,y} q(y|x) * p(x) * f_i(x, y)
        # Likeihood: L(p) = \sum_{x,y} p(x,y) * log( q(y|x) )
        self.model_expectations = [0] * model.feature_size
        correct_instance_count = 0
        log_likelihood = 0
        for instance in instances:
            label, self.condition_probabilities = \
                    self.ComputeConditionProbability(instance, model)
            #print 'label select:', label
            #print 'self.condition_probabilities:', self.condition_probabilities
            if label == instance.label:
                correct_instance_count += 1
            for feature in instance.features:
                context_id = model.context_id_map[feature.context]
                for i in range(len(model.labels)):
                    label = model.labels[i]
                    label_id = model.label_id_map[label]
                    feature2 = Feature(feature.context, label, 0)
                    if feature2 in model.feature_id_map:
                        feature_id = model.feature_id_map[feature2]
                        self.model_expectations[feature_id] += \
                                self.condition_probabilities[label_id] * \
                                self.context_counts[context_id] / \
                                self.sum_count * feature.value
                label_id2 = model.label_id_map[instance.label]
                log_condition_probability = \
                        self.__SafeLog(self.condition_probabilities[label_id2])
                log_likelihood += 1.0 / self.sum_count * \
                        log_condition_probability
        #print 'self.model_expectations:', self.model_expectations
        correct_rate = float(correct_instance_count) / self.sum_count
        return correct_rate, log_likelihood

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
            if feature in model.feature_id_map:
                feature_id = model.feature_id_map[feature]
                parameters[feature_id] = \
                        model.parameters[feature_id] + \
                        1.0 / self.correct_constant * \
                        self.__SafeLog(self.__SafeDiv(
                                self.empirical_expectations[feature_id],
                                self.model_expectations[feature_id]))
        #print 'parameters:', model.parameters
        model.parameters = parameters
        #print 'parameters update:', model.parameters

    def __IsConverged(self, new_log_likelihood):
        # TODO: fix
        return False
        if abs(float(new_log_likelihood - self.log_likelihood) / \
                self.log_likelihood) < self.error_threshold:
            return True
        return False

    def __SafeDiv(self, a, b):
        if a == 0:
            return 0.0
        if b == 0:
            return float(a) / self.zero
        return float(a) / b

    def __SafeLog(self, x):
        if x == 0:
            return self.log_zero
        return math.log(float(x))