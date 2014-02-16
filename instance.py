#!/usr/bin/env python
import logging
from feature import Feature

class Instance:
    def __init__(self):
        self.label = None
        # One instance contains n different features which belong
        # to different feature functions.
        self.features = []
        self.count = 0

    def __lt__(self, other):
        if self.label < other.label:
            return True
        elif self.label > other.label:
            return False
        if len(self.features) < len(other.features):
            return True
        elif len(self.features) > len(other.features):
            return False
        for i in range(len(self.features)):
            if self.features[i] < other.features[i]:
                return True
            elif self.features[i] > other.features[i]:
                return False
        return self.count < other.count

    def __eq__(self, other):
        if self.label != other.label:
            return False
        if len(self.features) != len(other.features):
            return False
        for i in range(len(self.features)):
            if self.features[i] != other.features[i]:
                return False
        return True

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        result = 'label:' + self.label + '\nfeatures:[\n'
        for feature in self.features:
            result += '    ' + str(feature) + ','
        result += '\n]\ncount:' + str(self.count)
        return result

    def LoadFromText(self, line):
        fields = line.split()
        if len(fields) < 2:
            logging.error('Fields number less than 2.')
            return False
        self.label = fields[0]
        for field in fields[1:]:
            sub_fields = field.split(':')
            value = 1.0
            if len(sub_fields) == 2:
                try:
                    value = float(sub_fields[1])
                except:
                    value = 1.0
            feature = Feature(sub_fields[0], self.label, value)
            self.features.append(feature)
        self.features.sort()
        self.count = 1
        return True
