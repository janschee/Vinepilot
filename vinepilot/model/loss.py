import torch

from vinepilot.config import Project

class VinePilotLoss():
    def __init__(self) -> None:
        self.available_losses: dict = {"mse": self.mse(), "poly_iou": self.poly_IoU}
        assert Project.loss in self.available_losses.keys(), f"Unknown loss in config file! Choose from {list(self.available_losses.keys())}!"
        self.loss = self.available_losses[Project.loss]

    def mse(self):
        return torch.nn.MSELoss()

    def poly_IoU(self):
        raise NotImplementedError

    def __call__(self):
        return self.loss