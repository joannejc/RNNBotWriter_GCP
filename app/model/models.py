import torch
from torch import nn

class RNN(nn.Module):
    def __init__(self, chars_size, embedding_size, hidden_size, n_layers=1, rnn_type='gru'):
        '''RNN model creation
        '''
        super().__init__()
        self._chars_size = chars_size # this is our vocabulary size, i.e 100
        self._embedding_size = embedding_size # this is our embedding size, i.e the output size of embedding our sparse
        self._hidden_size = hidden_size # hidden size for the hidden rnn
        self._n_layers = n_layers
        
        # create layers. If rnn_type is gru, use gru
        self.embedding = nn.Embedding(chars_size, embedding_size)
        if rnn_type == 'gru':
            self.rnn = nn.GRU(embedding_size, hidden_size, n_layers)
        else:
            raise NotImplementedError # this is to be implemented, for example replace with lstm
        self.h2o = nn.Linear(hidden_size, chars_size) # the hidden to output layer
        
    def forward(self, x, h):
        """Given an x and a hidden h, forward pass through our network. Our final output should be a softmax prediction
        over all the vocabulary.
        
        Args:
            x: input of shape [seq_len] x will be a long tensor of size seq_len, essentially a list of integers ranging from
            0 to 100, i.e x = [0, 5, 24, 0, 66]
            h: h_0** of shape `(num_layers * num_directions, batch, hidden_size)`
        
        """
        # step 1, get sequence length
        seq_len = x.size()[0]
        # step 2. pass our input through our embedding layer, and get the output "embed", reshape it via view to get
        # it ready for the rnn layer
        embed = self.embedding(x).view(seq_len, 1, -1) # rnn takes input of shape [seq_len x batch_size x input_dim]
        # step 3. forward pass our embed through our rnn layers, make sure to pass in hidden as well
        rnn_out, hidden = self.rnn(embed, h) # compute the rnn output
        # step 4: using our rnn output, pass it through the i2o(input to output) linear layer (remember to reshape to 2D)
        # and get the non-normalized output prediction
        prediction = self.h2o(rnn_out.view(seq_len,-1))
        # step 5: normalize our prediction by taking the log_softmax
        log_softmax = torch.nn.functional.log_softmax(prediction, dim=1)
        # return log softmax prediction and hidden
        return log_softmax, hidden
    
    def init_hidden(self):
        return torch.zeros(self._n_layers, 1, self._hidden_size)