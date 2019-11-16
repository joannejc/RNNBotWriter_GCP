import torch
from model.models import RNN
from model.utils import continue_words
from os import path
from path import Path
path = Path(__file__).parent
def getChars():
    ''' Get all characters used in the trained book (stored as 'chars.txt' when trained)
    '''
    file_path = path/"model"/"chars_v1.txt"
    with open(file_path) as f:
        chars = f.read()
    return chars


def getWeights():
    ''' Get trained weights from the Pytorch file
    '''
    file_path = path/"model"/"frankenstein_v1.pt"
    weights = torch.load(file_path, map_location=lambda storage, location:storage)
    return weights


def cleanUserWords(words, chars):
    ''' Remove any character in words that does not exist in chars.
    '''
    for w in words:
        if chars.find(w) == -1:
            words = words.replace(w,"")
    return words


def botWriter(words, sentence_len = 200):
    chars = getChars()
    weights = getWeights()
    # create a RNN model of the same chars_size, embedding_size, hidden_size, n_layers used in training
    model = RNN(len(chars), 100, 150, 2)
    model.load_state_dict(weights)  # update model weights
    words = cleanUserWords(words,chars) # pre-process user's words
    return continue_words(net=model, chars=chars, initial_word=words, sentence_len=sentence_len)
