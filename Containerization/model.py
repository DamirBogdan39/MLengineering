import torch
import torch.nn as nn
import torch.nn.functional as F


# Creating a classifier neural network class
class Clf(nn.Module):

    def __init__(self, input_features=4, hidden_layer1=25, hidden_layer2=30, output=3):
        super().__init__()
        self.fc1 = nn.Linear(input_features, hidden_layer1)
        self.fc2 = nn.Linear(hidden_layer1, hidden_layer2)
        self.out = nn.Linear(hidden_layer2, output)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.out(x)
        return x


# Setting up device
device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)

# Defining learning rate
learning_rate = 0.01


# Defining batch size
batch_size = 8


# Defining loss function
loss_fn = nn.CrossEntropyLoss()
