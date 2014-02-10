#!/usr/bin/env python

import pickle
from feature import *

class Model:
    def __init__(self):
        self.parameters = []
        self.cutoff = 1
        self.feature_size = 0
        self.labels = []
        self.contexts = []
        self.feature_map = {}

    def InitFromInstances(self, instances):
        label_map = {}
        context_map = {}
        for instance in instances:
            for feature in instance.features:
                self.AddFeature(feature)
                if feature.label not in label_map:
                    label_map[feature.label] = 1
                    self.labels.append(feature.label)
                if feature.context not in context_map:
                    context_map[feature.context] = 1
                    self.contexts.append(feature.context)

        # TODO: Delete feature by |cutoff|.

        self.feature_size = len(self.feature_map)
        self.parameters = [0.0] * self.feature_size

    def Load(self, model_name):
        input_file = open(model_name, 'rb')
        model = pickle.load(input_file)
        input_file.close()
        self = model

    def Save(self, model_name):
        print 'save'
        print 'model_name:', model_name
        output = open(model_name, 'wb')
        pickle.dump(self, output)
        output.close()

    def SetCutoff(self, cutoff):
        self.cutoff = cutoff

    def AddFeature(self, feature):
        if feature not in self.feature_map:
            self.feature_map[feature] = [feature]
        else:
            self.feature_map[feature].append(feature)

if __name__ == '__main__':
    pass