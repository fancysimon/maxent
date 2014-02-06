#!/usr/bin/env python
import logging
from feature import Feature

class Instance:
    def __init__(self):
        self.label = None
        self.features = []

    def LoadFromText(self, line):
        self.features = []
        fields = line.split()
        if len(fields) < 2:
            logging.error('Fields number less than 2.')
            return False
        self.label = fields[0]
        i = 0
        for field in fields[1:]:
            sub_fields = field.split(':')
            weight = 1.0
            if len(sub_fields) == 2:
                weight = float(sub_fields[1])
            feature = Feature(i, sub_fields[0], self.label, weight)
            self.features.append(feature)
            i += 1
        return True

    def FeatureSize(self):
        return len(self.features)
