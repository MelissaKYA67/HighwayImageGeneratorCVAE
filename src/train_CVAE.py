import torch
import os, time, tqdm
from CVAE import loss, cVAE
from utils import EarlyStop
from highwaydataset import dataloader


############## loading data ###################

train_iter = dataloader()
# , test_iter

############## loading models ###################

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

net = cVAE((3, 192, 256), 21, nhid=16, ncond=32)
net.to(device)
print(net)
save_name = "cVAE.pt"

############### training #########################

lr = 0.001
optimizer = torch.optim.Adam(filter(lambda p: p.requires_grad, net.parameters()), lr=lr, weight_decay=0.0001)


def adjust_lr(optimizer, decay_rate=0.95):
    for param_group in optimizer.param_groups:
        param_group['lr'] *= decay_rate


retrain = True
if os.path.exists(save_name):
    print("Model parameters have already been trained before. Retrain ? (y/n)")
    ans = input()
    if not (ans == 'y'):
        checkpoint = torch.load(save_name, map_location=device)
        net.load_state_dict(checkpoint["net"])
        optimizer.load_state_dict(checkpoint["optimizer"])
        for g in optimizer.param_groups:
            g['lr'] = lr

max_epochs = 1000
early_stop = EarlyStop(patience=20, save_name=save_name)
net = net.to(device)

print("training on ", device)
for epoch in range(max_epochs):

    train_loss, recon_loss, KLD_loss, n, start = 0.0, 0.0, 0.0, 0, time.time()
    for X, y in tqdm.tqdm(train_iter, ncols=50):
        X = X.to(device).float()
        y = y.to(device)
        X_hat, mean, logvar = net(X, y)

        l = loss(X, X_hat, mean, logvar).to(device)
        optimizer.zero_grad()
        l.backward()
        optimizer.step()

        train_loss += l.cpu().item()
        n += X.shape[0]

    train_loss /= n
    # print('epoch %d, train loss %.4f, time %.1f sec'
    #       % (epoch, train_loss, time.time() - start))
    print('epoch %d, train loss %10.6E, time %.1f sec'
          % (epoch, train_loss, time.time() - start))

    adjust_lr(optimizer)

    if (early_stop(train_loss, net, optimizer)):
        break

checkpoint = torch.load(early_stop.save_name)
net.load_state_dict(checkpoint["net"])