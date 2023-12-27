import torch
import torchvision

class PrintLayer(torch.nn.Module):
    def __init__(self):
        super(PrintLayer, self).__init__()

    def forward(self, x):
        print(x.shape)
        return x

""" 
class UpSample(torch.nn.Module):
    def __init__(self, scale_factor):
        super(UpSample, self).__init__()
        self.scale_factor = scale_factor

    def forward(self, x):
        return torch.nn.functional.interpolate(x, scale_factor=self.scale_factor, mode="nearest")
""" 
    
class Reshape(torch.nn.Module):
    def __init__(self, shape):
        super().__init__()
        self.shape = shape

    def forward(self, x):
        return torch.reshape(x, self.shape)

class SegmantationModel(torch.nn.Module):
    def __init__(self):
        super(SegmantationModel, self).__init__()

        self.encoder = torch.nn.Sequential(
            torch.nn.Conv2d(1, 32, kernel_size=(3, 3), stride=2, padding=1),
            torch.nn.ReLU(),
            torch.nn.Conv2d(32, 16, kernel_size=(3, 3), stride=2, padding=1),
            torch.nn.ReLU(),
            torch.nn.Conv2d(16, 8, kernel_size=(3, 3), stride=2, padding=1),
            torch.nn.ReLU(),
        )

        self.fully_connected = torch.nn.Sequential(
            torch.nn.Flatten(),
            torch.nn.Linear(8 * 16 * 32, 512),
            torch.nn.ReLU(),
            torch.nn.Linear(512, 512),
            torch.nn.ReLU(),
            Reshape((5, 1, 16, 32)) #TODO: Dont use fixed shapes!
        )

        self.decoder = torch.nn.Sequential(
            torch.nn.ConvTranspose2d(1, 1, kernel_size=(3, 3), stride=2, padding=1),
            PrintLayer(),
            torch.nn.ReLU(),
            torch.nn.ConvTranspose2d(1, 1, kernel_size=(3, 3), stride=2, padding=1),
            torch.nn.ReLU(),
            torch.nn.ConvTranspose2d(1, 1, kernel_size=(3, 3), stride=2, padding=1),
            torch.nn.ReLU(),
        )


    def forward(self, input):
        #Convert to Grayscale
        grayscale = torchvision.transforms.Grayscale(num_output_channels=1)
        x = grayscale(input)

        x = self.encoder(x)
        x = self.fully_connected(x)
        x = self.decoder(x) 

        return x






