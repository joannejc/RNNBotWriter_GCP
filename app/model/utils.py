import torch
import numpy as np
import random
import string
import torch.nn as nn
from torch import distributions
from .models import RNN #from models import RNN (for training)

def getSequence(book, sequence_size):
    ''' Extract random batch of characters as a single string
    '''
    index_0 = random.randint(0, len(book) - sequence_size)
    return book[index_0:(index_0 + sequence_size + 1)]


def test_words(net, chars, setence_len=50, iscuda = False):
    ''' Given a network, valid characters in trained book, let the network generate a sentence.
        This is used for training rnn model.
    '''
    # create hidden state
    ho = net.init_hidden()
    # create random word index
    x_in = torch.LongTensor([random.randint(0,len(chars)-1)])
    # create output index
    output = [int(x_in)]

    if iscuda:
        ho = ho.cuda()
        x_in = x_in.cuda()

    # now we iterate through our setence, pasing x_in to get y_out, and setting y_out as x_in for the next time step
    for i in range(setence_len):
        y_out, ho = net.forward(x_in, ho)
        dist = distributions.Categorical(probs=y_out.exp())
        # get max val and index
        sample = dist.sample()
        output.append(int(sample))
        x_in = sample
        
    # now we print our words
    words = ''
    for item in output:
        words += chars[item]
    return words


def continue_words(net, chars, initial_word, sentence_len=50):
    # create hidden state
    ho = net.init_hidden()
    # turn our word into index
    x_in = torch.zeros(len(initial_word)).long()
    for i, ch in enumerate(initial_word):
        x_in[i] = chars.find(ch)

    # create output index
    output = [chars.find(x) for x in initial_word]
    output.append(chars.find(' '))

    # forward pass our network through it first
    y_out, ho = net.forward(x_in, ho)
    y_out = y_out[-1,:].view(1,-1)
    dist = distributions.Categorical(probs=y_out.exp())
    x_in = dist.sample()
    # now we iterate through our sentence, passing x_in to get y_out & setting y_out as x_in for the next time step
    for i in range(sentence_len):
        y_out, ho = net.forward(x_in, ho)
        dist = distributions.Categorical(probs=y_out.exp())
        # get max val and index
        sample = dist.sample()
        output.append(int(sample))
        x_in = sample
        
    # now we print our words
    words = ''
    for item in output:
        words += chars[item]
    return words
