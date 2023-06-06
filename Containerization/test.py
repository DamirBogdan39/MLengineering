# Necessary imports

import pandas as pd
import torch
from torch.utils.data import DataLoader

from model import Clf, device, batch_size, loss_fn


# Read the test_df
df = pd.read_csv('data/test_df.csv')
X = df.drop(['Target'],axis=1).values
y = df['Target'].values


# Transforming the data into tensors
X_test = torch.FloatTensor(X)
y_test = torch.LongTensor(y)


# Defining test dataloader
test_dataloader = DataLoader(list(zip(X_test, y_test)), shuffle=True, batch_size=batch_size)


# Define testing
def test(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= num_batches
    correct /= size
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")


# Creating a model
model = Clf()


# Loading the weights of the NN
model.load_state_dict(torch.load('model.pth'))


# Testing with the model
epochs = 10
for epoch in range(epochs):
    print(f"Epoch {epoch+1}\n-------------------------------")
    test(test_dataloader, model, loss_fn)
print("Done with testing!")
