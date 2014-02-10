#!/usr/bin/env python
import logging
from feature import Feature

class Instance:
    def __init__(self):
        self.label = None
        # One instance contains n different features which belong
        # to different feature functions.
        self.features = []

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
                value = float(sub_fields[1])
            feature = Feature(sub_fields[0], self.label, value)
            self.features.append(feature)
        return True
