import torch
import torchvision

class PrintLayer(torch.nn.Module):
    def __init__(self):
        super(PrintLayer, self).__init__()

    def forward(self, x):
        print(x.shape)
        return x


class SegmentationModel(torch.nn.Module):
    def __init__(self):
        super(SegmentationModel, self).__init__()

        # Encoder
        self.encoder = torch.nn.Sequential(
            torch.nn.Conv2d(1, 32, kernel_size=3, stride=2, padding=1),
            torch.nn.ReLU(inplace=True),
            torch.nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),
            torch.nn.ReLU(inplace=True),
            torch.nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),
            torch.nn.ReLU(inplace=True),
        )

        # Bottleneck
        self.bottleneck = torch.nn.Sequential(
            torch.nn.Linear(128 * 16 * 32, 512, bias=True),
            torch.nn.ReLU(inplace=True),
            torch.nn.Linear(512, 512),
            torch.nn.ReLU(inplace=True),
        )

        # Decoder
        self.decoder = torch.nn.Sequential(
            torch.nn.ConvTranspose2d(512, 128, kernel_size=(2,4), stride=(2,4)),
            torch.nn.ReLU(inplace=True),
            torch.nn.ConvTranspose2d(128, 64, kernel_size=4, stride=4),
            torch.nn.ReLU(inplace=True),
            torch.nn.ConvTranspose2d(64, 32, kernel_size=4, stride=4),
            torch.nn.ReLU(inplace=True),
            torch.nn.ConvTranspose2d(32, 1, kernel_size=4, stride=4),
            torch.nn.ReLU(inplace=True),
            torch.nn.Conv2d(1, 1, kernel_size=3, stride=1, padding=1),
            torch.nn.Sigmoid(),
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
        x = x.view(x.size(0), 512, 1, 1)

        # Decoder
        x = self.decoder(x)

        # Post-processing to convert probability values to [0, 255]
        x = (x * 255).round()

        return x
