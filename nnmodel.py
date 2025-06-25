import torch.nn as nn, torch.nn.functional as func, torch.optim as optim # import relevant libraries

class HGCNN(nn.Module):
    def __init__(self):
        super.__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=20, kernel_size=9, stride=1, padding=0) # 1 x 28 x 28 input layer to 20 feature maps, each producing 20 x 20 output
        self.conv2 = nn.Conv2d(in_channels=20, out_channels=48, kernel_size=5, stride=1, padding=0) # 20 x 10 x 10 input layer to 48 feature maps, each producing 6 x 6 output
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0) # max pooling layer, max of each 2x2 grid
        self.fc1 = nn.Linear(in_features=48*3*3, out_features=46) # FC layer, reading 48 x 3 x 3 (432) inputs to produce 46 outputs

    def forward(self, x):
        x = self.pool(func.relu(self.conv1(x))) # apply relu activation to conv1 output & pool
        x = self.pool(func.relu(self.conv2(x))) # apply relu activation to conv2 output & pool
        x = x.view(-1, 48*3*3) # flatten the output from 48 grids of 3x3 feature map outputs to a single vector of size 432
        x = self.fc1(x) # apply the fully connected layer to the vector and produce 46 outputs
        return x

lossfunc = nn.CrossEntropyLoss() # loss function for training, cross entropy loss
optimizer = optim.SGD(HGCNN.parameters(), lr=0.01, momentum=0.9, weight_decay=0.0005) # optimizer for training, stochastic gradient descent with learning rate 0.01 and momentum 0.9
