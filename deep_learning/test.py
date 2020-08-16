
import sys
import os
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms,datasets
import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import cv2
from torchvision.datasets import ImageFolder
import numpy as np

transforms_train = transforms.Compose([transforms.ToTensor(),transforms.Normalize([0.5,0.5,0.5],[0.5,0.5,0.5])])
image_data_test = ImageFolder("./finalimg3",transform=transforms_train)

#transforms_mul = transforms.Compose([transforms.RandomResizedCrop(size=100),#剪出随机大小和随机高宽比的一块随机区域，然后将该区域缩放为高和宽均为100像素的输入
#                                     transforms.Resize(size=256),#将图像的高和宽均缩放为256像素
#                                     transforms.CenterCrop(size=224),#裁剪出高和宽均为224像素的中心区域作为输入
#                                     transforms.ToTensor(),
#                                     transforms.Normalize([0.5,0.5,0.5],[0.5,0.5,0.5])
#                                    ])

bsz = 64 # eval(input("Input batch_size: "))
# to batch
test_loader = DataLoader(dataset=image_data_test,batch_size=1)



classes = ('Apple','Apple', 'Apple','Apple','Apple','Apple','Apple','Apple','Apple','Apple',
'Apple','Apple','Apple','Apricot','Avocado','Avocado','Banana','Banana','Banana','Beetroot',
'Blueberry','Cactus_Fruit','Cantaloupe','Cantaloupe','Carambula','Cauliflower','Cherry','Cherry',
'Cherry','Cherry','Cherry','Cherry','Chestnut','Clementine','Cocos','Corn','Corn','Cucumber',
'Cucumber','Dates','Eggplant','Fig','Ginger','Granadilla','Grape','Grape','Grape','Grape','Grape',
'Grape','Grapefruit','GrapeFruit','Guava','Hazelnut','Huckleberry','Kaki','Kiwi','Kohlrabi',
'Kumquats','Lemon','Lemon','Limes','Lychee','Mandarine','Mango','Mango','Mangostan','Maracuja',
'Melon','Mulberry','Nectarine','Nectarine','Nut','Nut','Onion','Onion','Onion','Orange','Papaya',
'Passion_Fruit','Peach','Peach','Peach','Pear','Pear','Pear','Pear','Pear','Pear','Pear','Pear','Pear',
'Pepino','Pepper','Pepper','Pepper','Pepper','Physalis','Physalis','Pineapple','Pineapple','Pitahaya',
'Plum','Plum','Plum','Pomegranate','Pomelo_Sweetie','Potato','Potato','Potato','Potato','Quince',
'Rambutan','Raspberry','Redcurrant','Salak','Strawberry','Strawberry','Tamarillo','Tangelo','Tomato',
'Tomato','Tomato','Tomato','Tomato','Tomato','Tomato','Tomato','Tomato','Walnut','Watermelon')
# print(classes)
# exit()


# Flatten Layer
class Flatten(nn.Module):
    def forward(self, x):
        return x.view(x.size(0), -1)
    
# define our model
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        # conv2d parameters: in_channels, out_channels, kernel_size, stride
        # input shape: (bsz, 1, 28, 28)
#         self.conv = nn.Conv2d(in_channels=1,
#                               out_channels=32,
#                               kernel_size=3,
#                               stride=1,
#                               padding=1)
#         # output shape: (bsz, 32, 28, 28)
#         self.dropout1 = nn.Dropout2d(0.2)
#         self.dropout2 = nn.Dropout(0.4)
#         self.relu = nn.ReLU()
#         self.pool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
#         # output shape: (bsz, 32, 14, 14)
#         self.fc1 = nn.Linear(6272, 128)
#         self.fc2 = nn.Linear(128, 10)
        # 64,3,100,100
        self.seq = nn.Sequential(
                                 nn.Conv2d(3, 64, kernel_size=5),
                                 nn.ReLU(),
                                 nn.MaxPool2d(2),# 64,64,50,50
#                                 nn.Dropout(0.2),
                                 nn.Conv2d(64, 64, kernel_size=7, stride=1),
                                 nn.ReLU(),
                                 nn.MaxPool2d(3),
#                                 nn.Dropout(0.2),
                                 nn.Conv2d(64, 64, kernel_size=7),
                                 nn.ReLU(),
                                 nn.MaxPool2d(5),
#                                 nn.Dropout(0.2),
                                 Flatten(),
                                 nn.Linear(64, 1024),
                                 nn.ReLU(),
                                 nn.Linear(1024, 256),
                                 nn.ReLU(),
                                 nn.Linear(256, 4))
        
    
    def forward(self, x):
#         x = self.conv(x) #(bsz, 1, 28, 28) -> (bsz, 32, 28, 28)
#         x = self.relu(x)
#         x = self.pool(x) #-> (bsz, 32, 14, 14)
#         x = self.dropout1(x)
#         x = torch.flatten(x, 1) #->(bsz, 6272)
#         x = self.fc1(x) #->(bsz, 128)
#         x = self.relu(x)
#         x = self.dropout2(x)
#         x = self.fc2(x) #->(bsz, 10) ##raw logits
        model = self.seq(x)
        return model
        


# define our training function
def train(model, device, train_loader, optimizer, epoch):
    model.train()
    loss_fn = nn.CrossEntropyLoss()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        output = model(data)
        loss = loss_fn(output, target)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if batch_idx % 200 == 0:
            print ('Train Epoch: {}, Batch Index: {}, Loss: {}'.format(
                epoch, batch_idx, loss.item()))
        
        
# define out testing function
def test(model, device, test_loader):
    model.eval()
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            pred = output.argmax(dim=1,) #(bsz,)
            correct += pred.eq(target).sum().item()
    print (" Test Accuracy: {}%".format(
            correct/len(test_loader.dataset)*100))

# write a predict function to do prediction
def predict(model, img):
    model.eval()
    output = model(torch.reshape(img,(1,3,100,100)))
    pred = output.argmax(dim=1,)
    return pred.item()

SAVE_PATH = "mnist_cnn.ckpt"
## load the model
model = Net()
model.load_state_dict(torch.load(SAVE_PATH, map_location=torch.device('cpu')))
print("finish_load")
num = len(image_data_test)
# print(num)

for x in range(num):
    # index = np.random.randint(0,3,size=1)[0]
    img, lab = image_data_test[x]
    # print("index: ", index)
    print ("actual Label:", lab)
    print ("Model prediction:", predict(model, img))
