#!/usr/bin/env python

class Feature:
    def __init__(self, index, name, label, weight=1.0):
        self.index = str(index)
        self.name = name
        self.label = label
        self.weight = weight

    def __eq__(self, other):
        if self.index == other.index and self.name == other.name and self.label == other.label:
            return True
        return False

    def __hash__(self):
        return hash((self.index, self.name, self.label))

class FeatureDict:
    def __init__(self):
        self.feature_dict = {}

    def AddFeature(self, feature):
        if feature not in self.feature_dict:
            self.feature_dict[feature] = feature.weight
        else:
            self.feature_dict[feature] += feature.weight

    def Size(self):
        return len(self.feature_dict)

if __name__ == '__main__':
    a = Feature(1, 'a', 'b')
    b = Feature(1, 'a', 'b')
    c = Feature('1', 'a', 'b')
    d = Feature(11, 'a', 'b')
    print a == b
    print a == c
    print a == d
    aa = {}
    aa[a] = 1
    print b in aa
    print c in aa
    print d in aa