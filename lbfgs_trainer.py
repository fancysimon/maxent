#!/usr/bin/env python
from trainer import Trainer

class LBFGSTrainer(Trainer):
    def Train(self, instances, model, iterations):
        print 'iters   loglikelihood    training accuracy'
        print '=========================================='
        print '=========================================='
        return