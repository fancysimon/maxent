#!/usr/bin/env python
from optimizer import Optimizer

class GisOptimizer(Optimizer):
    def __init__(self):
        self.expectation_for_instance = {}

    def EstimateParamater(self, model):
        __ComputeExpectationForInstance(model.features, model.sum_weight)

    def __ComputeExpectationForInstance(self, features, sum_weight):
        for feature in features:
            self.expectation_for_instance[feature] = feature.weight / sum_weight

    def __ComputeExpectationForModel(self):