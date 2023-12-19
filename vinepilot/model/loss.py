import torch

class VinePilotLoss():
    def __init__(self, loss: str) -> None:
        self.available_losses: dict = {"mse": self.mse, "poly_iou": self.poly_IoU}
        assert loss in self.available_losses.keys(), f"Unknown loss! Choose from {list(self.available_losses.keys())}!"
        self.loss_fn: callable = self.available_losses[loss]

    def mse(self):
        return torch.nn.MSELoss()

    def poly_IoU(self):
        raise NotImplementedError

    def __call__(self):
        return self.loss_fn()