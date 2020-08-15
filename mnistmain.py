# -*- coding: utf-8 -*-
import torch
import math
from mlxtend.data import loadlocal_mnist
from mnist_common import *
import time

batch_size = 10000
learning_rate = 1e-3

save_model = "mnist-conv10-40-classifier.model"
#load_model = save_model
load_model = None

x_data, y_data = loadlocal_mnist(
    images_path='train-images.idx3-ubyte', 
    labels_path='train-labels.idx1-ubyte')
x = torch.tensor(x_data, dtype=torch.float32)
x = x.reshape(x.shape[0],1,28,28)
y = torch.tensor(y_data,dtype = torch.int64)

test_x_data, test_y_data = loadlocal_mnist(
    images_path='t10k-images.idx3-ubyte', 
    labels_path='t10k-labels.idx1-ubyte')
test_x = torch.tensor(test_x_data, dtype=torch.float32)
test_x = test_x.reshape(test_x.shape[0],1,28,28)
test_y = torch.tensor(test_y_data, dtype=torch.int64)


model = ConvNet()

print("network created")
if load_model!=None:
    try:
        model.load_state_dict(torch.load(load_model))
        model.eval()
    except:
        print("failed to load model. using new model")
loss_fn = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

t=0
while True:
    #timer = time.time()
    correct_amount = 0
    for i in range(int(x.shape[0]/batch_size)):
        #print(i)
        y_pred = model(x[batch_size*i:batch_size*(i+1)])
        loss = loss_fn(y_pred, y[batch_size*i:batch_size*(i+1)])
        #print(y_pred,loss)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        y_pred_argmax = y_pred.argmax(1)
        for i in range(len(y_pred_argmax)):
            if y_pred_argmax[i]==y_data[i]:
                correct_amount += 1
    #y_pred = model(x)
    #loss = loss_fn(y_pred, y)
    ##print(y_pred,loss)
    #optimizer.zero_grad()
    #loss.backward()
    #optimizer.step()
    #print("time taken:",time.time()-timer)
    if t % 1 == 0:
        with torch.set_grad_enabled(False):
            print_loss = loss.item()
            test_y_pred = model(test_x)
            test_loss = loss_fn(test_y_pred,test_y)
            print_training_acc = (correct_amount*100.0)/len(y)
            #print(correct_amount,len(y))
            test_y_pred_argmax = test_y_pred.argmax(1)
            test_correct_amount = 0
            for i in range(len(test_y_pred_argmax)):
                if test_y_pred_argmax[i]==test_y_data[i]:
                    test_correct_amount += 1
            print_testing_acc = (test_correct_amount*100.0)/len(test_y_pred_argmax)
            print(correct_amount,len(test_y_pred_argmax))
            print("epoch:",t,"loss: {:.5f}".format(print_loss),
                "train acc: {:.2f}%".format(print_training_acc),
                "testing acc: {:.2f}%".format(print_testing_acc))
            if save_model!=None:
                torch.save(model.state_dict(), save_model)
        
    t+=1