import torch.nn as nn, torch.nn.functional as func

class HGCNN(nn.Module): # my first neural network!!!
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=9, stride=1, padding=0) # 1 x 28 x 28 input layer to 32 feature maps, each producing 20 x 20 output
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=80, kernel_size=5, stride=1, padding=0) # 32 x 10 x 10 input layer to 80 feature maps, each producing 6 x 6 output
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0) # max pooling layer, max of each 2x2 grid
        self.fc1 = nn.Linear(in_features=80*3*3, out_features=46) # FC layer, reading 80 x 3 x 3 (720) inputs to produce 46 outputs

    def forward(self, x):
        x = self.pool(func.relu(self.conv1(x))) # apply relu activation to conv1 output & pool
        x = self.pool(func.relu(self.conv2(x))) # apply relu activation to conv2 output & pool
        x = x.view(-1, 80*3*3) # flatten the output from 80 grids of 3x3 feature map outputs to a single vector of size 720
        x = self.fc1(x) # apply the fully connected layer to the vector and produce 46 outputs
        return x
