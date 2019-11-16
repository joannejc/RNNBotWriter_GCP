import torch
import numpy as np
import random
import string
import torch.nn as nn
#from torch import distributions
from models import RNN
from utils import getSequence, test_words

# Load data, extact all sentences and unique character set
filename = "Frankenstein.txt"

with open(filename,"r") as read_file:
        rawbook = read_file.read()

# Raw book data processing and cleaning
book = rawbook.replace('\n',' ') # string
chars = "".join(set(book)) # get a string of unique characters used in the book
chars += " "
chars_len = len(chars) 

# Save chars to txt file:
with open('chars_v2.txt', 'w') as chars_file:
    chars_file.write(chars)


# Main Training Loop
def main():
    epochs = 301
    seq_batch_size = 200
    print_yes = 100
    iscuda = False

    # create our network, optimizer and loss function
    net = RNN(len(chars), 100, 150, 2) #instanciate a RNN object
    optim = torch.optim.Adam(net.parameters(),lr=6e-4)
    loss_func = torch.nn.functional.nll_loss

    if iscuda:
        net = net.cuda()

    # main training loop:
    for epoch in range(epochs):
        dat = getSequence(book, seq_batch_size)
        dat = torch.LongTensor([chars.find(item) for item in dat]) #find corresponding char index for each character and store this in tensor
        
        # pull x, y and initialize hidden state
        if iscuda:
            x_t = dat[:-1].cuda()
            y_t = dat[1:].cuda()
            hidden = net.init_hidden().cuda()
        else:
            x_t = dat[:-1]
            y_t = dat[1:]
            hidden = net.init_hidden()

        # forward pass
        logprob, hidden = net.forward(x_t, hidden)
        loss = loss_func(logprob, y_t)
        # update
        optim.zero_grad()
        loss.backward()
        optim.step()
        # print the loss for every kth iteration
        if epoch % print_yes == 0:
            print('*'*60)
            print('\n epoch {}, loss:{} \n'.format(epoch, loss))
            print('sample speech:\n', test_words(net, chars, seq_batch_size))

    torch.save(net.state_dict(), 'trainedBook_v2.pt')

if  __name__== "__main__":
    main()