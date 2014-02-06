#!/usr/bin/env python

from feature import *

class Model:
    def __init__(self):
        self.parameters = []
        self.features = []
        self.feature_dict = FeatureDict()
        self.cutoff = 1
        self.sum_weight = 0

    def InitFromInstances(self, instances):
        for instance in instances:
            for feature in instance.features:
                self.feature_dict.AddFeature(feature)
        self.parameters = [0.0] * self.feature_dict.Size()
        for feature in self.feature_dict:
            weight = self.feature_dict[feature.weigth = ]
            feature.weight = weight
            self.sum_weight += weight
            self.features.append(feature)

    def Load(self, model_name):
        pass

    def Save(self, model_name):
        pass

    def SetCutoff(self, cutoff):
        self.cutoff = cutoff

if __name__ == '__main__':
    pass