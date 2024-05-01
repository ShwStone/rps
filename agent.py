from network import Network
import torch
import random

def baseVec(dim :int, pos: int) -> torch.Tensor :
    res = torch.zeros(dim)
    res[pos] = 1
    return res

class Agent :
    def __init__(self) -> None:
        self.history = []
        self.memory = []
        self.length = 8
        self.epochs = 8
        self.range = 64

        self.model = Network(6, 3)
        self.lossFunc = torch.nn.MSELoss()
        self.optimizer = torch.optim.Adam(self.model.parameters())

    def round(self) :
        if len(self.history) >= self.length :
            inputs = torch.stack(self.history[-self.length:])
            with torch.no_grad() :
                predicts = self.model(inputs)

            return (torch.argmax(predicts).item() + 2) % 3
        
        else :
            return random.randint(0, 2)
        
    def update(self) :
        size = min(len(self.memory), self.range)
        inputs, outputs = map(torch.stack, tuple(zip(*self.memory[-size:])))
        inputs = inputs.swapaxes(0, 1)
        for t in range(self.epochs) :
            self.optimizer.zero_grad()
            predicts = self.model(inputs)
            loss = self.lossFunc(predicts, outputs)
            loss.backward()
            self.optimizer.step()

    def result(self, playerAction, agentAction, result) :
        if len(self.history) >= self.length :
            self.memory.append((
                torch.stack(self.history[-self.length:]),
                baseVec(3, playerAction)
            ))
            self.update()

        self.history.append(
            torch.concatenate((
                baseVec(3, playerAction), 
                baseVec(3, agentAction)
            ))
        )
