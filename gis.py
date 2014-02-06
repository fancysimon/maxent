#!/usr/bin/env python
from optimizer import Optimizer

class Gis(Optimizer):
    def EstimateParamater(self, instances):
        return [1.0] * instances[0].FeatureSize()