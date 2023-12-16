import torch

from vinepilot.config import Project

class VinePilotOptimizer():
    def __init__(self, trainable_parameters) -> None:
        self.available_optimizers: dict = {"adam": self.adam}
        assert Project.optimizer in self.available_optimizers.keys(), f"Unknown optimizer in config file! Choose from {list(self.available_optimizers.keys())}!"
        self.optimizer: callable = self.available_optimizers[Project.optimizer]
        self.parameters = trainable_parameters

    def adam(self):
        return torch.optim.Adam(params=self.parameters, lr=Project.learning_rate)

    def __call__(self):
        return self.optimizer()