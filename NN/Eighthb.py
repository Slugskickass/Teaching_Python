#import requests
import matplotlib.pyplot as plt
import numpy as np
#import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import torchvision
import torchvision.transforms as transforms


train_set = torchvision.datasets.FashionMNIST(
    root='./data'
    ,train=True
    ,download=True
    ,transform=transforms.Compose([
        transforms.ToTensor()
    ])
)

train_loader = torch.utils.data.DataLoader(train_set
    ,batch_size=10
    ,shuffle=True
)

torch.set_grad_enabled(True)
class Network(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=6, kernel_size=5)
        self.conv2 = nn.Conv2d(in_channels=6, out_channels=12, kernel_size=5)

        self.fc1 = nn.Linear(in_features=12 * 4 * 4, out_features=120)
        self.fc2 = nn.Linear(in_features=120, out_features=60)
        self.out = nn.Linear(in_features=60, out_features=10)

    def forward(self, t):
        t = t
        print(t.shape)

        # (2) hidden conv layer
        t = self.conv1(t)
        # in 28 x 28
        # out 24 x 24
        t = F.relu(t)
        t = F.max_pool2d(t, kernel_size=2, stride=2)
        # out 12 * 12
        print(t.shape)

        # (3) hidden conv layer
        t = self.conv2(t)
        # in 12 * 12
        # out 8 x 8
        t = F.relu(t)
        t = F.max_pool2d(t, kernel_size=2, stride=2)
        # out 4 x 4
        print(t.shape)

        # (4) hidden linear layer
        t = t.reshape(-1, 12 * 4 * 4)
        print(t.shape)
        t = self.fc1(t)
        t = F.relu(t)
        print(t.shape)

        # (5) hidden linear layer
        t = self.fc2(t)
        t = F.relu(t)
        print(t.shape)

        # (6) output layer
        t = self.out(t)
        t = F.softmax(t, dim=1)
        print(t.shape)

        return t

    def __repr__(self):
        return "Bunny Kitten"

network = Network()

batch = next(iter(train_loader))
images, labels = batch

preds = network(images)

print(preds.argmax(dim=1))
print(labels)
print(preds.argmax(dim=1).eq(labels))
print(preds.argmax(dim=1).eq(labels).sum())