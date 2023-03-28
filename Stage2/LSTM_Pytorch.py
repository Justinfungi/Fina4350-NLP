#!/usr/bin/env python
# coding: utf-8

# In[46]:


import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt


# #Alpha vantage
# 
# 2OQT6WT9WH45WTK5

# In[226]:


myticker = "AAPL"
df = pd.read_csv(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={myticker}&apikey=2OQT6WT9WH45WTK5&datatype=csv')
df


# In[261]:


df1 = df.reset_index()["close"]
df1.shape


# In[57]:


df1.plot()
plt.show()


# In[58]:


scaler = MinMaxScaler(feature_range=(0,1))
df1 = scaler.fit_transform(np.array(df1).reshape(-1,1))
df1


# In[59]:


plt.plot(df1)
plt.show()


# In[60]:


scaler.inverse_transform(df1[1].reshape(-1, 1))


# # Dataset

# In[227]:


df_len = int(len(df1))
training_size = int(df_len * 0.65)
testing_size = df_len - training_size
train_data,test_data=df1[0:training_size,:],df1[training_size:len(df1),:1]


# In[249]:


class StockDataset(Dataset):
    def __init__(self,data,seq_len = 20):
        self.data = data
        self.data = torch.from_numpy(data).float().view(-1)
        self.seq_len = seq_len
        
    def __len__(self):
        return len(self.data)-self.seq_len-1

    def __getitem__(self, index) : # start from x and prediction is x+20
        # return x, y
        return  self.data[index : index+self.seq_len] , self.data[index+self.seq_len]


train_dataset = StockDataset(train_data) 
test_dataset = StockDataset(test_data)
full_dataset = StockDataset(df1)


# In[276]:


batch_size = 4
train_dataloader = DataLoader(train_dataset,batch_size,drop_last=True)
test_dataloader = DataLoader(test_dataset,batch_size,drop_last=True)
full_dataloader = DataLoader(full_dataset,batch_size,drop_last=True)

device = "cuda" if torch.cuda.is_available() else "cpu"

count = 0
for data in train_dataloader:
    count +=1
    print(data[1].shape)
print(count)
print(training_size)
# so the total should be 44 y for 65 data points
# 20 lookback


# # Model

# In[238]:


class Lstm_model(nn.Module):
    def __init__(self, input_dim , hidden_size , num_layers):
        super(Lstm_model, self).__init__()
        self.num_layers = num_layers
        self.input_size = input_dim
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size=input_dim , hidden_size = hidden_size , num_layers= num_layers )
        self.fc = nn.Linear(hidden_size,1)

    def forward(self,x,hn,cn):
        out , (hn,cn) = self.lstm(x , (hn,cn))
        final_out = self.fc(out[-1])
        return final_out,hn,cn

    def predict(self,x):
        hn,cn  = self.init()
        out , (hn,cn) = self.lstm(x , (hn,cn))
        final_out = self.fc(out[-1])
        return final_out

    def init(self):
        h0 =  torch.zeros(self.num_layers , batch_size , self.hidden_size).to(device)
        c0 =  torch.zeros(self.num_layers , batch_size , self.hidden_size).to(device)
        return h0 , c0


input_dim = 1 
hidden_size = 50
num_layers = 3
model = Lstm_model(input_dim , hidden_size , num_layers).to(device)


# In[239]:


loss_fn = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)


# In[232]:


def train(dataloader):
    hn , cn = model.init()
    model.train()
    for batch , item in enumerate(dataloader):
        x , y = item
        x = x.to(device)
        y = y.to(device)
        # x in shape of seq_len, batch size, 1
        out , hn , cn = model(x.reshape(20,batch_size,1),hn,cn) 
        loss = loss_fn(out.reshape(batch_size) , y)
        hn = hn.detach()
        cn = cn.detach()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if batch == len(dataloader)-1:
            loss = loss.item()
            print(f"train loss: {loss:>7f} ")


# In[279]:


def test(dataloader):
    res = torch.tensor([], dtype=torch.int64)
    hn , cn = model.init()
    model.eval()
    for batch , item in enumerate(dataloader):
        x , y = item
        x = x.to(device)
        y = y.to(device)
        out , hn , cn = model(x.reshape(20,batch_size,1),hn,cn)
        #print(out)
        res =  torch.cat((out,res), 0) 
        loss = loss_fn(out.reshape(batch_size) , y)
       
        if batch == len(dataloader)-1:
            loss = loss.item()
            print(f"test loss: {loss:>7f} ")
                  
    return res


# In[280]:


epochs = 200
for epoch in range(epochs):
    print(f"epoch {epoch} ")
    train(train_dataloader)
    output0 = test(train_dataloader)
    output = test(test_dataloader)


# In[291]:


print(output.shape)
res = output.detach().numpy()
print(res.shape)


# In[297]:


#res = np.concatenate((output0.detach().numpy(),output.detach().numpy()))
res1 = scaler.inverse_transform(res)
plt.plot(np.arange(93,105,1),np.array(res1))
plt.plot(df1)


# In[236]:


import math
from sklearn.metrics import mean_squared_error
import numpy as np
def calculate_metrics(data_loader):
    pred_arr = []
    y_arr = []
    with torch.no_grad():
        hn , cn = model.init()
        for batch , item in enumerate(data_loader):
            x , y = item
            x , y = x.to(device) , y.to(device)
            x = x.view(20,4,1)
            pred = model(x,hn,cn)[0]
            pred = scaler.inverse_transform(pred.detach().cpu().numpy()).reshape(-1)
            y = scaler.inverse_transform(y.detach().cpu().numpy().reshape(1,-1)).reshape(-1)
            pred_arr = pred_arr + list(pred)
            y_arr = y_arr + list(y)
        print(pred_arr[11],y_arr[11])
        return math.sqrt(mean_squared_error(y_arr,pred_arr))
    


# In[237]:


# calculating final loss metrics
print(f"train mse loss {calculate_metrics(train_dataloader)}")
print(f"test mse loss {calculate_metrics(test_dataloader)}")

