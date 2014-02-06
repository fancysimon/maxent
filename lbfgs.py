#!/usr/bin/env python
from optimizer import Optimizer

class LbfgsOptimizer(Optimizer):
    def EstimateParamater(self, model):
        return