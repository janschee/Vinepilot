import torch
import torchvision

class PrintLayer(torch.nn.Module):
    def __init__(self):
        super(PrintLayer, self).__init__()

    def forward(self, x):
        print(x.shape)
        return x
    

class UpSample(torch.nn.Module):
    def __init__(self, scale_factor):
        super(UpSample, self).__init__()
        self.scale_factor = scale_factor

    def forward(self, x):
        return torch.nn.functional.interpolate(x, scale_factor=self.scale_factor, mode="nearest")
    

class SegmantationModel(torch.nn.Module):
    def __init__(self):
        """
        self.convDOWN = torch.nn.Conv2d(1, 1, kernel_size=5, stride=1, padding=0)        
        self.convUP = torch.nn.Conv2d(1, 1, kernel_size=5, stride=1, padding=4)
        self.convCONST = torch.nn.Conv2d(1, 1, kernel_size=5, stride=1, padding=2)
        self.relu = torch.nn.ReLU()  
        """
        super(SegmantationModel, self).__init__()
        self.encoder = torch.nn.Sequential(
            torch.nn.Conv2d(1, 8, kernel_size=(3, 3), stride=2, padding=1),
            torch.nn.ReLU(),
            torch.nn.Conv2d(8, 16, kernel_size=(3, 3), stride=2, padding=1),
            torch.nn.ReLU(),
            torch.nn.Conv2d(16, 32, kernel_size=(3, 3), stride=2, padding=1),
            torch.nn.ReLU(),
        )
        self.decoder = torch.nn.Sequential(
            UpSample(scale_factor=2),
            torch.nn.Conv2d(32, 16, kernel_size=(3, 3), stride=1, padding=1),
            torch.nn.ReLU(),
            UpSample(scale_factor=2),
            torch.nn.Conv2d(16, 8, kernel_size=(3, 3), stride=1, padding=1),
            torch.nn.ReLU(),
            UpSample(scale_factor=2),
            torch.nn.Conv2d(8, 1, kernel_size=(3, 3), stride=1, padding=1),
            torch.nn.ReLU(),
        )


    def forward(self, input):
        #Convert to Grayscale
        grayscale = torchvision.transforms.Grayscale(num_output_channels=1)
        x = grayscale(input)

        x = self.encoder(x)
        x = self.decoder(x) 

        return x






