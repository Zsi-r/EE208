'''Fit a curve with PyTorch.'''
from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
import torch

from models import Naive_NN

NUM_TRAIN_SAMPLES = 200
NUM_TRAIN_EPOCHS = 8000  # try: 100, 1000, 10000, 50000
LEARNING_RATE = 0.001 #try: 1 ,0.1 , 0.01 ,0.001

torch.manual_seed(2019)#设定生成随机数的种子

def my_f(x):
    return 0.5*x**3 + np.sin(x) -1


def f(x):
    """Actual function (ground truth)."""
    return x**2 + 2 * np.sin(x) + np.cos(x - 1) - 5

# Create dataset


class MyDataset(torch.utils.data.Dataset):
    def __init__(self):
        super(MyDataset, self).__init__()
        self.x, self.y = self.generate_data(NUM_TRAIN_SAMPLES)

    def generate_data(self, num):
        # Generate num training data disturbed by noise.
        x = (torch.rand([num, 1]) - 0.5) * 10.0 # num行1列,0~1之间，-0.5对半分，*10使得落在-5~5
        y_noise = my_f(x) + torch.randn([num, 1]) * 7
        return x, y_noise

    def get_all_data(self):
        return self.x.detach(), self.y.detach()

    def __len__(self):
        return NUM_TRAIN_SAMPLES

    def __getitem__(self, index):
        return self.x[index], self.y[index]


model = Naive_NN()
dataset = MyDataset()
dataloader = torch.utils.data.DataLoader(dataset, batch_size=200, shuffle=True)
optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)#solving stochastic problem

# train
model.train()
for epoch in range(NUM_TRAIN_EPOCHS):
    loss_avg = []
    for x, target_y in dataloader:
        # Reset gradients
        model.zero_grad()
        # Forward pass
        predicted_y = model(x)
        # Calc loss (mean squared error)
        mse = (predicted_y - target_y)**2
        loss = torch.mean(mse)
        # Backward pass (determine the weights' updating direction)
        loss.backward()
        # Apply weight updating with certain learning rate
        optimizer.step()#loss.backward()和optimizer.step()配套使用
        # Monitor loss
        loss_avg.append(torch.sum(mse).detach())
    print('Epoch [%d/%d], Loss=%f' %
          (epoch + 1, NUM_TRAIN_EPOCHS, sum(loss_avg) / len(dataset)))#sum向量里各张量求和

# save model
torch.save(model.state_dict(), 'model.pth')

# test curve
model.eval()
with torch.no_grad():
    x = torch.linspace(-5, 5, 50).reshape([50, 1])#-5~5 生成等距的50份
    y = model(x)
    plt.plot(x, y, color='y', label='learnt curve')  # learnt curve
    plt.plot(x, my_f(x), color='r', label='ground-truth curve')  # ground-truth curve
    plt.scatter(*(dataset.get_all_data()), label='training set')  # training set
    plt.legend()
    plt.show()
