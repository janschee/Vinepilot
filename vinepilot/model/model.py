import torch
import torchvision

class PrintLayer(torch.nn.Module):
    def __init__(self):
        super(PrintLayer, self).__init__()

    def forward(self, x):
        print(x.shape, x.dtype)
        return x

class Interpolate(torch.nn.Module):
    def __init__(self, scale_factor):
        super(Interpolate, self).__init__()
        self.scale_factor = scale_factor

    def forward(self, x):
        return torch.nn.functional.interpolate(x, scale_factor=self.scale_factor, mode="bilinear")

class Multiply(torch.nn.Module):
    def __init__(self, alpha):
        super().__init__()
        self.alpha =  alpha
    
    def forward(self, x):
        x = torch.mul(x, self.alpha)
        return x

class SegmentationModel(torch.nn.Module):
    def __init__(self):
        super(SegmentationModel, self).__init__()

        # Encoder
        self.encoder = torch.nn.Sequential(
            torch.nn.Conv2d(1, 32, kernel_size=3, stride=2, padding=1),
            torch.nn.ReLU(inplace=True),
            torch.nn.Conv2d(32, 32, kernel_size=3, stride=2, padding=1),
            torch.nn.ReLU(inplace=True),
            torch.nn.Conv2d(32, 32, kernel_size=3, stride=2, padding=1),
            torch.nn.ReLU(inplace=True),
        )

        # Bottleneck
        self.bottleneck = torch.nn.Sequential(
            torch.nn.Linear(32 * 16 * 32, 1024, bias=False),
            torch.nn.ReLU(inplace=True),
            torch.nn.Linear(1024, 512, bias=True),
            torch.nn.ReLU(inplace=True),
            torch.nn.Linear(512, 512, bias=True),
            torch.nn.ReLU(inplace=True),
        )

        # Decoder
        self.decoder = torch.nn.Sequential(
            Interpolate(scale_factor=2),
            torch.nn.Conv2d(1, 1, kernel_size=3, stride=1, padding=1),
            torch.nn.ReLU(inplace=True),
            Interpolate(scale_factor=2),
            torch.nn.Conv2d(1, 1, kernel_size=3, stride=1, padding=1),
            torch.nn.ReLU(inplace=True),
            Interpolate(scale_factor=2),
            torch.nn.Conv2d(1, 1, kernel_size=3, stride=1, padding=1),
            torch.nn.ReLU(inplace=True),
            torch.nn.Tanh(),
            Multiply(255),
        )

    def forward(self, x):
        # Convert to Grayscale
        x = torchvision.transforms.Grayscale(num_output_channels=1)(x)

        # Encoder
        x = self.encoder(x)

        # Flatten
        x = x.view(x.size(0), -1)

        # Bottleneck
        x = self.bottleneck(x)

        # Reshape for decoder
        x = x.view(x.size(0), 1, 16, 32)

        # Decoder
        x = self.decoder(x)

        return x
