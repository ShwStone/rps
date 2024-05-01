import torch
import torch.nn as nn
import torch.nn.functional as F

class Network(nn.Module) :
    def __init__(self, n, m) -> None:
        super(Network, self).__init__()
        self.n, self.m = n, m

        self.rnn = nn.RNN(n, 64)
        self.classifier = nn.Linear(64, m)

    def forward(self, inputs) :
        outs, hidden = self.rnn(inputs)
        x = self.classifier(outs[-1])
        outputs = F.softmax(x, -1)
        return outputs
    
if __name__ == '__main__' :
    a = Network(6, 3)
    x = torch.tensor([[[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]]).type(torch.FloatTensor)
    print(a(x))