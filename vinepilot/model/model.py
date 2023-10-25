import torch
import torchvision

class TrackDetectionModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        
        #Set1
        self.conv_layer1 = torch.nn.Conv2d(in_channels=1, out_channels=1, kernel_size=3, stride=1, padding=2)
        self.conv_layer2 = torch.nn.Conv2d(in_channels=1, out_channels=1, kernel_size=3, stride=1, padding=2)
        self.max_pool1 = torch.nn.MaxPool2d(kernel_size=3, stride=3)

        #Set2
        self.conv_layer3 = torch.nn.Conv2d(in_channels=1, out_channels=1, kernel_size=3, stride=1, padding=0)
        self.conv_layer4 = torch.nn.Conv2d(in_channels=1, out_channels=1, kernel_size=3, stride=1, padding=0)
        self.max_pool2 = torch.nn.MaxPool2d(kernel_size=3, stride=3)

        #Set3
        self.fc1 = torch.nn.Linear(672, 200)
        self.relu1 = torch.nn.ReLU()
        self.fc2 = torch.nn.Linear(200, 8)

    def forward(self, input):
        #Resize image
        resize = torchvision.transforms.Resize((200, 300), antialias=True)
        x = resize(input) #torch.Size([1, 1, 200, 300])

        #Convert to Grayscale
        grayscale = torchvision.transforms.Grayscale(num_output_channels=1)
        x = grayscale(x)

        #Set1
        x = self.conv_layer1(x)
        x = self.conv_layer2(x)
        x = self.max_pool1(x)

        #Set2
        x = self.conv_layer3(x)
        x = self.conv_layer4(x)
        x = self.max_pool2(x)

        #Flatten output
        x = torch.reshape(x, (-1,)) #torch.Size([672])

        #Set3
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        
        return torch.reshape(x, (1,4,2))




