#!/usr/bin/env python
import sys
import argparse
import logging
from common import *
from instance import Instance
from gis import Gis

def ParseOptions():
    parser = argparse.ArgumentParser(description='Maxent')
    parser.add_argument("-m", "--model",
                        dest="model",
                        default="",
                        help="Model file for maxent.")
    parser.add_argument("-p", "--predict", action="store_true", 
                        dest="predict", 
                        default=False, 
                        help="Predict.")
    parser.add_argument("-i", "--iter",
                        dest="iter",
                        default=30,
                        help="Iterations for training algorithm. default=30",
                        type=int)
    parser.add_argument("-o", "--output",
                        dest="output",
                        default="",
                        help="Output file.")
    
    options = parser.parse_args()
    if options.model == '':
        print 'model must be specified.'
        parser.print_help()
        sys.exit(1)
    if options.predict:
        if options.output == '':
            print 'output must be specified when predict.'
            parser.print_help()
            sys.exit(1)
    return options

def LoadInstances():
    field_num = -1
    instances = []
    print 'LoadInstances'
    for line in sys.stdin:
        line = line.rstrip('\n')
        if line == '':
            break
        instance = Instance()
        instance.LoadFromText(line)
        if field_num == -1:
            field_num = instance.FeatureSize()
        else:
            if field_num != instance.FeatureSize():
                logging.error('Fields number is not equal.')
                return None
        instances.append(instance)
    print 'LoadInstances end'
    return instances

def Train(options):
    instances = LoadInstances()
    if instances == None:
        logging.error('Training instances format is not valid.')
        sys.exit(1)

def Predict(options):
    pass

def Main():
    options = ParseOptions()
    logging.basicConfig(
            level=logging.DEBUG,
            format='[%(asctime)s %(filename)s:%(lineno)d] [%(levelname)s]: %(message)s',
            datefmt='%a, %d %b %Y %H:%M:%S',
            filemode='w')
    if options.predict:
        Predict(options)
    else:
        Train(options)

if __name__ == '__main__':
    Main()