#!/usr/bin/env python

class Feature:
    def __init__(self, context, label, value):
        self.context = context
        self.label = label
        self.value = value

    def __eq__(self, other):
        if self.context == other.context and self.label == other.label:
            return True
        return False

    def __hash__(self):
        return hash((self.context, self.label))

# class FeatureMap:
#     def __init__(self):
#         # Feature is feature function. One feature may contain many 
#         # feature instances.
#         self.feature_map = {}
#         self.sum_value = 0

#     def AddFeature(self, feature):
#         if feature not in self.feature_map:
#             self.feature_map[feature] = [feature]
#         else:
#             self.feature_map[feature].append(feature)
#         self.sum_value += feature.value

#     def SumValue(self):
#         return self.sum_value

#     def Size(self):
#         return len(self.feature_map)