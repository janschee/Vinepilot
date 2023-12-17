import torch
import torchvision

class SegmantationModel(torch.nn.Module):
    def __init__(self):
        super().__init__()

        self.convDOWN = torch.nn.Conv2d(1, 1, kernel_size=5, stride=1, padding=0)        
        self.convUP = torch.nn.Conv2d(1, 1, kernel_size=5, stride=1, padding=4)
        self.convCONST = torch.nn.Conv2d(1, 1, kernel_size=5, stride=1, padding=2)

        self.relu = torch.nn.ReLU()   

    def forward(self, input):
        x = input

        #Convert to Grayscale
        grayscale = torchvision.transforms.Grayscale(num_output_channels=1)
        x = grayscale(x)

        #Encoder
        x = self.convDOWN(x)
        x = self.relu(x)
        x = self.convDOWN(x)
        x = self.relu(x)

        #Tunnel
        x = self.convCONST(x)
        x = self.relu(x)
        x = self.convCONST(x)
        x = self.relu(x)
        x = self.convCONST(x)
        x = self.relu(x)
        x = self.convCONST(x)
        x = self.relu(x)
        x = self.convCONST(x)
        x = self.relu(x)

        #Decoder
        x = self.convUP(x)
        x = self.relu(x)
        x = self.convUP(x)
        x = self.relu(x)

        return x






