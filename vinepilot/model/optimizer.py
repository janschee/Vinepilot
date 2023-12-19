import torch

class VinePilotOptimizer():
    def __init__(self, optimizer: str, learning_rate: float, trainable_parameters) -> None:
        self.available_optimizers: dict = {"adam": self.adam}
        assert optimizer in self.available_optimizers.keys(), f"Unknown optimizer in config file! Choose from {list(self.available_optimizers.keys())}!"
        self.optimizer: callable = self.available_optimizers[optimizer]
        self.parameters = trainable_parameters
        self.learning_rate = learning_rate

    def adam(self):
        return torch.optim.Adam(params=self.parameters, lr=self.learning_rate)

    def __call__(self):
        return self.optimizer()