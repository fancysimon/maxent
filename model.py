#!/usr/bin/env python

from feature import *

class Model:
    def __init__(self):
        self.parameters = []
        self.feature_dict = FeatureDict()

    def InitFromInstances(self, instances):
        for instance in instances:
            for feature in instance.features:
                self.feature_dict.AddFeature(feature)
        self.parameters = [0.0] * self.feature_dict.Size()

if __name__ == '__main__':
    pass