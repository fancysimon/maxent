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
        self.feature_id_map = {}
        self.context_id_map = {}
        self.label_id_map = {}

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

        # Generate |feature_id|, |context_id| and |label_id|.
        feature_id = 0
        context_id = 0
        for feature in self.feature_map:
            self.feature_id_map[feature] = feature_id
            feature_id += 1
            if feature.context not in self.context_id_map:
                self.context_id_map[feature.context] = context_id
                context_id += 1
        label_id = 0
        for label in self.labels:
            self.label_id_map[label] = label_id
            label_id += 1

    @staticmethod
    def Load(model_name):
        input_file = open(model_name, 'rb')
        model = pickle.load(input_file)
        input_file.close()
        return model

    def Save(self, model_name):
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