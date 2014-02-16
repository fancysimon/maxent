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

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.context, self.label))

    def __lt__(self, other):
        if self.label < other.label:
            return True
        elif self.label > other.label:
            return False
        if self.context < other.context:
            return True
        elif self.context > other.context:
            return False
        return self.value < other.value

    def __str__(self):
        return 'label:' + self.label + ' context:' + self.context + ' value:' + str(self.value)

if __name__ == '__main__':
    feature_list = [Feature('context2', 'lebel2', 1),
                    Feature('context1', 'lebel1', 1),
                    Feature('context3', 'lebel3', 1)]
    feature_list.sort()
    for feature in feature_list:
        print feature