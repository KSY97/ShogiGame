import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.backends.cudnn as cudnn
import torch.optim as optim
import os
import numpy as np

from dual_network import DN_INPUT_SHAPE

from pathlib import Path
from dual_network import ResNet18, PATH
import pickle

from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader
from torch.utils.data.sampler import SubsetRandomSampler

# 파라미터 준비
RN_EPOCHS = 1000  # 학습 횟수
BATCH_SIZE = 512
patience_limit = 20

def load_data():
  history_path = sorted(Path('./data').glob('*.history'))[-1]
  with history_path.open(mode='rb') as f:
    return pickle.load(f)

def train_network():
  model = ResNet18()
  model.load_state_dict(torch.load(PATH))

  cudnn.benchmark = True
  optimizer = optim.Adam(model.parameters(), weight_decay=0.0002)

  train(model, optimizer)

  torch.save(model.state_dict(), './model/latest.h5')

  del model

def train(model, optimizer):
  device = 'cuda'
  model = model.to(device)
  model = torch.nn.DataParallel(model)

  history = load_data()
  xs, y_policies, y_values = zip(*history)
  xs = np.array(xs, dtype=np.float32)
  y_policies =np.array(y_policies, dtype = np.float32)
  y_values =np.array(y_values, dtype = np.float32)
  # print(xs.shape)
  # print(len(xs))
  a, b, c = DN_INPUT_SHAPE

  xs = xs.reshape(len(xs), a, b, c)
  # print(xs.shape)
  xs = torch.tensor(xs)
  y_policies = torch.tensor(y_policies)
  y_values = torch.tensor(y_values)

  valid_size = 0.2
  num_train = len(xs)
  indices = list(range(num_train))
  split = int(np.floor(valid_size * num_train))
  train_idx, valid_idx = indices[split:], indices[:split]
  
  # print('train_idx = ', train_idx)
  # print('valid_idx = ', valid_idx)

  train_sampler = SubsetRandomSampler(train_idx)
  valid_sampler = SubsetRandomSampler(valid_idx)

  dataset = TensorDataset(xs, y_policies, y_values)
  train_loader = DataLoader(dataset, batch_size= BATCH_SIZE ,sampler=train_sampler)
  val_loader = DataLoader(dataset, batch_size= BATCH_SIZE ,sampler=valid_sampler)
  # print(len(dataloader))

  # dataloader = DataLoader(dataset, batch_size= BATCH_SIZE, shuffle=True)
  best_loss1 = 10**5
  best_loss2 = 10**5

  for i in range(RN_EPOCHS):
    torch.cuda.empty_cache()
    for batch_idx, samples in enumerate(train_loader):
      print("\r Epochs : {} - batch_idx : {}/{}".format(i+1, batch_idx + 1, len(train_loader)), end='')

      xs, y_policies, y_values = samples

      # print('xs = ', xs.dtype)
      # print('torch.max(y_policies) = ', torch.max(y_policies))
      # print('y_values = ', y_values)

      xs = xs.clone().detach().requires_grad_(True)
      y_policies = y_policies.clone().detach().requires_grad_(True)
      y_values = y_values.clone().detach().requires_grad_(True)

      # print('xs = ', xs)
      # print('torch.max(y_policies) = ', torch.max(y_policies))
      # print('y_values = ', y_values)

      xs = xs.to(device=device)
      y_policies = y_policies.to(device=device)
      y_values = y_values.to(device=device)

      optimizer.zero_grad()
      # model.train()
      model.eval()
      with torch.no_grad():
        p, v = model(xs)

      v = v.reshape(len(v))
      # print(p.dtype)
      # print(v.dtype)
      # xs = xs.type(torch.LongTensor)
      # y_policies = y_policies.long()
      # y_values = y_values.type(torch.LongTensor)
      # p = p.long()
      # v = v.type(torch.LongTensor)

      # print('y_policies = ',y_policies)
      # print('p =', p)

      model.train()
      celoss = nn.CrossEntropyLoss()
      mseloss = nn.MSELoss()
      loss1 = celoss(p, y_policies)
      loss2 = mseloss(v, y_values)
      
      loss1.backward(retain_graph=True)
      loss2.backward()

      optimizer.step()

    val_loss1 = 0
    val_loss2 = 0

    for batch_idx, samples in enumerate(val_loader):
      xs, y_policies, y_values = samples

      xs = xs.to(device)
      y_policies = y_policies.to(device)
      y_values = y_values.to(device)

      model.eval()
      with torch.no_grad():
        p, v = model(xs)

      v = v.reshape(len(v))

      celoss = nn.CrossEntropyLoss()
      mseloss = nn.MSELoss()
      loss1 = celoss(p, y_policies)
      loss2 = mseloss(v, y_values)
      
      val_loss1 += loss1.item()
      val_loss2 += loss2.item()
    
    if val_loss1 > best_loss1 and val_loss2 > best_loss2: # loss가 개선되지 않은 경우
      patience_check += 1

      if patience_check >= patience_limit: # early stopping 조건 만족 시 조기 종료
        print('\nEarly Stop')
        # model = ResNet18()
        model.load_state_dict(torch.load('./model/temp.h5'))
        break

    else: # loss가 개선된 경우
      best_loss1 = val_loss1
      best_loss2 = val_loss2
      patience_check = 0

      torch.save(model.state_dict(), './model/temp.h5')


  

# 동작 확인
if __name__ == '__main__':
    train_network()