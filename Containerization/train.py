# Necessary imports

import pandas as pd
import torch
from torch.utils.data import DataLoader

from model import Clf, device, batch_size, loss_fn, learning_rate

# Read the train_df

df = pd.read_csv('data/train_df.csv')
X = df.drop(['Target'],axis=1).values
y = df['Target'].values

# Transforming the data into tensors

X_train = torch.FloatTensor(X)
y_train = torch.LongTensor(y)


# Creating a model object, defining learning rate, loss and optimizer
model = Clf()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)


# Creating a dataloader
train_dataloader = DataLoader(list(zip(X_train, y_train)), shuffle=True, batch_size=batch_size)


# Defining a training function
def train(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    model.train()
    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)

        # Compute prediction error
        pred = model(X)
        loss = loss_fn(pred, y)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if batch % 1 == 0:
            loss, current = loss.item(), (batch + 1) * len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")


# Train the model
epochs = 10
for epoch in range(epochs):
    print(f"Epoch {epoch+1}\n-------------------------------")
    train(train_dataloader, model, loss_fn, optimizer)
print('Done with training!')

# Saving the model
torch.save(model.state_dict(), 'model.pth')
