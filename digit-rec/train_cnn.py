import torch
import torch.optim as optim
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms 


transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,),(0.5,))
])

trainset = torchvision.datasets.MNIST(root ='./data',train = True, download = True,transform = transform)
trainloader = torch.utils.data.DataLoader(trainset,batch_size=64,shuffle = True) 

class Net(nn.Module):
    def __init__(self):
        super(Net,self).__init__()
        self.conv1 = nn.Conv2d(1,32,3,1)
        self.conv2 = nn.Conv2d(32,64,3,1)
        self.fc1 = nn.Linear(9216,128)
        self.fc2 = nn.Linear(128,10)
    
    def forward(self,x):
        x = torch.relu(self.conv1(x)) 
        x = torch.relu(self.conv2(x))
        x = torch.max_pool2d(x,2,2)
        x = torch.flatten(x,1)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x
    

net = Net()

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(),lr = 0.001)

for epoch in range(1):
    for data,target in trainloader:
        optimizer.zero_grad()
        output = net(data)
        loss = criterion(output,target)
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch}, Loss: {loss.item()}")   


dummy_input = torch.randn(1,1,28,28)     

torch.onnx.export(net, dummy_input, "mnist_cnn.onnx",
                  input_names=['input'], output_names=['output'],
                  dynamic_axes={'input': {0: 'batch'}, 'output': {0: 'batch'}})
print("Model exported to mnist_cnn.onnx") 