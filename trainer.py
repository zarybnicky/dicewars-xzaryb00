import numpy as np
from os.path import dirname
import torch
import torch.nn as nn
from torch.autograd import Variable
from torch.optim import SGD
from torch.utils.data import Dataset, DataLoader

class AttacksDataset(Dataset):
    def __init__(self, csv_file):
        self.data = np.genfromtxt(csv_file, delimiter=',')

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        return (torch.from_numpy(self.data[idx, :-2]).float(),
                torch.from_numpy(self.data[idx, -2:]).float())

def main():
    model = nn.Sequential(
        nn.Linear(9, 8),
        nn.PReLU(),
        nn.Linear(8, 2),
    )
    dataset = AttacksDataset(dirname(__file__) + '/turns.csv')
    optimizer = SGD(model.parameters(), lr=0.01)
    loss_fn = nn.MSELoss(reduction='mean')
    loader = torch.utils.data.DataLoader(dataset=dataset, shuffle=True)

    for epoch in range(200):
        total_loss = 0
        for batch_idx, (x, target) in enumerate(loader):
            optimizer.zero_grad()
            out = model(x)
            loss = loss_fn(out, target)
            total_loss += loss.data.item()
            loss.backward()
            optimizer.step()
        print('epoch: {}, train loss: {:.6f}'.format(epoch, total_loss))

    torch.save(model.state_dict(), dirname(__file__) + '/local-predictor.model')

if __name__ == '__main__':
    main()
