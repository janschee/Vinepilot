import copy
import torch
import torchvision

class SegmantationModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        """
        self.convDOWN = torch.nn.Conv2d(1, 1, kernel_size=5, stride=1, padding=0)        
        self.convUP = torch.nn.Conv2d(1, 1, kernel_size=5, stride=1, padding=4)
        self.convCONST = torch.nn.Conv2d(1, 1, kernel_size=5, stride=1, padding=2)
        self.relu = torch.nn.ReLU()  
        """

        self.encoder = []
        for i in range(2):
            exec(f"self.encoder_conv{i} = torch.nn.Conv2d(1, 1, kernel_size=5, stride=1, padding=0)")
            exec(f"self.encoder.append(self.encoder_conv{i})")
            exec(f"self.encoder_relu{i} = torch.nn.ReLU()")
            exec(f"self.encoder.append(self.encoder_relu{i})")

        self.tunnel = []
        for i in range(10):
            exec(f"self.tunnel_conv{i} = torch.nn.Conv2d(1, 1, kernel_size=5, stride=1, padding=2)")
            exec(f"self.tunnel.append(self.tunnel_conv{i})")
            exec(f"self.tunnel_relu{i} = torch.nn.ReLU()")
            exec(f"self.tunnel.append(self.tunnel_relu{i})")
            
        self.decoder = []
        for i in range(2):
            exec(f"self.decoder_conv{i} = torch.nn.Conv2d(1, 1, kernel_size=5, stride=1, padding=4)")
            exec(f"self.decoder.append(self.decoder_conv{i})")
            exec(f"self.decoder_relu{i} = torch.nn.ReLU()")
            exec(f"self.decoder.append(self.decoder_relu{i})")



    def forward(self, input):
        #Convert to Grayscale
        grayscale = torchvision.transforms.Grayscale(num_output_channels=1)
        x = grayscale(input)

        #Encoder
        for layer in self.encoder: x = layer(x)

        #Tunnel
        for layer in self.tunnel: x = layer(x)

        #Decoder
        for layer in self.decoder: x = layer(x)

        return x






