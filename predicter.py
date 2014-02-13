from gis_trainer import GISTrainer
class Predicter:
    def Predict(self, instance, model):
        trainer = GISTrainer()
        label, probabilities = \
                trainer.ComputeConditionProbability(instance, model)
        return label, probabilities
        