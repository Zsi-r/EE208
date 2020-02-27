'''Train CIFAR-10 with PyTorch.'''
import os

import torch
import torch.backends.cudnn as cudnn
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms

from models import resnet20

start_epoch = 1
end_epoch = 4
lr = 0.1

# Data pre-processing, DO NOT MODIFY
print('==> Preparing data..')
transform_train = transforms.Compose([
    transforms.RandomCrop(32, padding=4),#Crop image: output (size,size) of the crop
    transforms.RandomHorizontalFlip(),#horizontally flip with the given probability
    transforms.ToTensor(),#Convert a PIL Image or numpy.ndarray to tensor.
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    #Normalize a tensor image with mean and standard deviation
])

transform_test = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])

trainset = torchvision.datasets.CIFAR10(
    root='./data', train=True, download=True, transform=transform_train)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=128, shuffle=True)

testset = torchvision.datasets.CIFAR10(
    root='./data', train=False, download=True, transform=transform_test)
testloader = torch.utils.data.DataLoader(testset, batch_size=128, shuffle=False)

classes = ("airplane", "automobile", "bird", "cat",
           "deer", "dog", "frog", "horse", "ship", "truck")

# Model
print('==> Building model..')
model = resnet20()
# If you want to restore training (instead of training from beginning),
# you can continue training based on previously-saved models
# by uncommenting the following two lines.
# Do not forget to modify start_epoch and end_epoch.
#restore_model_path = 'pretrained/ckpt_4_acc_63.320000.pth'
restore_model_path = 'mytrain/ckpt_0_acc_37.668000.pth'
model.load_state_dict(torch.load(restore_model_path)['net'])

# A better method to calculate loss
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=lr, weight_decay=5e-4)#Stochastic Gradient Descent (SGD)


def train(epoch):
    model.train()
    train_loss = 0
    correct = 0
    total = 0
    # trainloader长度为391 ，每次循环处理同一个批次的128张图片
    for batch_idx, (inputs, targets) in enumerate(trainloader):
                                              #targets:   tensor([5, 2, 9, 0, 0, 6, 2, 8, 8, 1, 6, 9, 0, 0, 8, 0])
        optimizer.zero_grad()#Sets gradients of all model parameters to zero.
        outputs = model(inputs)               #outputs:   tensor([[-0.8460,  2.6492,  1.3735,  ..., -1.7537,  4.0319,  0.5340]]
        # The outputs are of size [128x10].
        # 128 is the number of images fed into the model 
        # (yes, we feed a certain number of images into the model at the same time, 
        # instead of one by one)
        # For each image, its output is of length 10.
        # Index i of the highest number suggests that the prediction is classes[i].
        loss = criterion(outputs, targets)   #tensor(2.0603, grad_fn=<NllLossBackward>)

        loss.backward()
        optimizer.step()
        train_loss += loss.item()   # += 2.0603

        _, predicted = outputs.max(1) # the predicted tensors having 1 fewer dimension than output , a squeeze operation is done only in the given dimension
        total += targets.size(0)#targets.size(0)都是128,即batch size
        correct += predicted.eq(targets).sum().item()
        #eq对两个tensor中每个元素判断是否相等，以bool tensor的形式输出/
        #sum结果是如tensor(34),item后是34
        print('Epoch [%d] Batch [%d/%d] Loss: %.3f | Traininig Acc: %.3f%% (%d/%d)'
              % (epoch, batch_idx + 1, len(trainloader), train_loss / (batch_idx + 1),
                 100. * correct / total, correct, total))

    print('Saving trained model..')
    state = {
        'net': model.state_dict(),
        'acc': 100. * correct / total,
        'epoch': epoch,
    }
    if not os.path.isdir('mytrain'):
        os.mkdir('mytrain')
    torch.save(state, './mytrain/ckpt_%d_acc_%f.pth' % (epoch, 100. * correct / total))


def test(epoch):
    print('==> Testing...')
    model.eval()
    with torch.no_grad():
        total = 0
        correct = 0
        ##### TODO: calc the test accuracy #####
        # Hint: You do not have to update model parameters.
        #       Just get the outputs and count the correct predictions.
        #       You can turn to `train` function for help.
        for batch_idx, (inputs, targets) in enumerate(testloader):
            optimizer.zero_grad()#Sets gradients of all model parameters to zero.
            outputs = model(inputs)               #outputs:   tensor([[-0.8460,  2.6492,  1.3735,  ..., -1.7537,  4.0319,  0.5340]]

            _, predicted = outputs.max(1) # the predicted tensors having 1 fewer dimension than output , a squeeze operation is done only in the given dimension
            total += targets.size(0)#targets.size(0)都是128,即batch size
            correct += predicted.eq(targets).sum().item()
            #eq对两个tensor中每个元素判断是否相等，以bool tensor的形式输出/
            #sum结果是如tensor(34),item后是34
            print('Epoch [%d] Batch [%d/%d]| Traininig Acc: %.3f%% (%d/%d)'
                  % (epoch, batch_idx + 1, len(testloader),
                     100. * correct / total, correct, total))
        acc = 100. * correct / total
        ########################################
    # Save checkpoint.
    print('Test Acc: %f' % acc)
    print('Saving tested model..')
    state = {
        'net': model.state_dict(),
        'acc': acc,
        'epoch': epoch,
    }
    if not os.path.isdir('checkpoint'):
        os.mkdir('checkpoint')
    torch.save(state, './checkpoint/ckpt_%d_acc_%f.pth' % (epoch, acc))


for epoch in range(start_epoch, end_epoch + 1):
    train(epoch)
    test(epoch)
