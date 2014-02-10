#!/usr/bin/env python
import sys
import argparse
import logging
from common import *
from instance import Instance
from gis_trainer import GISTrainer
from model import Model

def ParseOptions():
    parser = argparse.ArgumentParser(description='Maxent. Read data from argv or stdin.')
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
    parser.add_argument("-a", "--algorithm",
                        dest="algorithm",
                        default="gis",
                        help="Algorithm to train maxent. gis or lbfgs. default=gis")
    parser.add_argument("-c", "--cutoff",
                        dest="cutoff",
                        default=1,
                        type=int,
                        help="Cutoff to select feature. default=1")
    parser.add_argument('input',
                        nargs='?',
                        type=argparse.FileType('r'),
                        default=sys.stdin)
    
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
    if options.algorithm != 'gis' and options.algorithm != 'lbfgs':
        print 'Training algorithm must be gis or lbfgs.'
        parser.print_help()
        sys.exit(1)
    return options

def LoadInstances(input_file):
    instances = []
    print 'LoadInstances'
    for line in input_file:
        line = line.rstrip('\n')
        if line == '':
            break
        instance = Instance()
        instance.LoadFromText(line)
        instances.append(instance)
    print 'LoadInstances end'
    return instances

def Train(options):
    instances = LoadInstances(options.input)
    if instances == None:
        logging.error('Training instances format is not valid.')
        sys.exit(1)
    model = Model()
    model.SetCutoff(options.cutoff)
    model.InitFromInstances(instances)
    trainer = None
    if options.algorithm == 'gis':
        trainer = GISTrainer()
    else:
        trainer = LBFGSTrainer()
    trainer.Train(instances, model, options.iter, options.model)
    model.Save(options.output)

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