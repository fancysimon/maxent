#!/usr/bin/env python
import sys
import argparse
import logging
from common import *
from instance import Instance
from gis_trainer import GISTrainer
from model import Model
from predicter import Predicter

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

def LoadInstances(input_file, cutoff):
    instances = []
    for line in input_file:
        line = line.rstrip('\n')
        if line == '':
            break
        instance = Instance()
        instance.LoadFromText(line)
        instances.append(instance)
    print 'Load %d instances.' % len(instances)
    if len(instances) == 0:
        print 'There must be more than 0 instances for training maxent model.'
        sys.exit(1)
    sys.stdout.flush()
    instances = MergeInstances(instances, cutoff)
    print 'There are %d instances after merging.' % len(instances)
    if len(instances) == 0:
        print 'There must be more than 0 instances for training maxent model.'
        sys.exit(1)
    return instances

def MergeInstances(instances, cutoff):
    # Merge instances.
    instances.sort()
    last_instance = instances[0]
    for i in range(1, len(instances)):
        instance = instances[i]
        if instance == last_instance:
            last_instance.count += instance.count
            instance.count = 0
        else:
            last_instance = instance
    # Delete feature by |cutoff| and delete feature with |count| equal 0.
    merged_instances = []
    for instance in instances:
        if instance.count >= cutoff:
            merged_instances.append(instance)
    return merged_instances

def Train(options):
    instances = LoadInstances(options.input, options.cutoff)
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
    trainer.Train(instances, model, options.iter)
    model.Save(options.model)

def Predict(options):
    prodicter = Predicter()
    model = Model.Load(options.model)
    instances = LoadInstances(options.input)
    output_file = open(options.output, 'w')
    correct_count = 0
    sum_count = 0
    for instance in instances:
        label, probabilities = prodicter.Predict(instance, model)
        if label == instance.label:
            correct_count += 1
        sum_count += 1
        output_file.write(label + '\t' + str(probabilities) + '\n')
    output_file.close()
    print float(correct_count) / sum_count

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