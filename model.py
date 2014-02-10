#!/usr/bin/env python

import pickle
from feature import *

class Model:
    def __init__(self):
        self.parameters = []
        self.cutoff = 1
        self.feature_size = 0
        self.feature_map = None
        self.labels = []
        self.contexts = []

    def InitFromInstances(self, instances):
        self.feature_map = FeatureMap()
        label_map = {}
        context_map = {}
        for instance in instances:
            for feature in instance.features:
                self.feature_map.AddFeature(feature)
                if feature.label not in label_map:
                    label_map[feature.label] = 1
                    self.labels.append(feature.label)
                if feature.name not in context_map:
                    context_map[feature.name] = 1
                    self.contexts.append(feature.name)

        # TODO: Delete feature by |cutoff|.

        self.feature_size = self.feature_map.Size()
        self.parameters = [0.0] * self.feature_size

    def Load(self, model_name):
        input_file = open(model_name, 'rb')
        model = pickle.load(input_file)
        input_file.close()
        self = model

    def Save(self, model_name):
        output = open(model_name, 'wb')
        pickle.dump(self, output)
        output.close()

    def SetCutoff(self, cutoff):
        self.cutoff = cutoff

if __name__ == '__main__':
    pass