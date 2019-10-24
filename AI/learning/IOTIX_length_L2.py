# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 15:44:44 2019

@author: bjiso
"""

import os
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import math
import json
from sklearn.metrics import mean_squared_error
from datetime import datetime
from keras.optimizers import Adam
 
look_back = 3
output_size=7

def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back):
        a = dataset[i:(i + look_back)]
        dataX.append(a)
        dataY.append(dataset[i + look_back])
    print(dataX[-1])
    print(dataY[-1])
    return np.array(dataX), np.array(dataY)

 
# file loader
with open('sample191020_5.json') as json_file:
    json_data = json.load(json_file)
print("file open")

arr=[]
for i in range(0, 100):
    arr.append(float(json_data['test'][i]['length']))
 
# convert nparray
nparr=np.array(arr)
nparr.astype('float32')
nparr = nparr.reshape(-1,1)
 
# normalization
scaler = MinMaxScaler(feature_range=(-1, 1))
nptf = scaler.fit_transform(nparr)
 
# split train, test
train_size = int(len(nptf) * 0.8)
test_size = len(nptf) - train_size
train, test = nptf[0:train_size], nptf[train_size:len(nptf)]
print(len(train), len(test))
 
# create dataset for learning
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)
 
# reshape input to be [samples, time steps, features]
trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
 
# simple lstm network learning
model = Sequential()
model.add(LSTM(16, input_shape=(1, look_back)))
model.add(Dense(1, activation='linear'))
model.compile(loss='mean_squared_error', optimizer=Adam(lr=0.05)) #lr 학습률
model.fit(trainX, trainY, epochs=500, batch_size=1, verbose=2)
 
# make prediction
trainPredict = model.predict(trainX)
trainPredict = scaler.inverse_transform(trainPredict)

testPredict = model.predict(testX)
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform(testY)
testScore = math.sqrt(mean_squared_error(testY, testPredict))
print('Train Score: %.2f RMSE' % testScore)

# plot
fig = plt.figure(facecolor='white')
plt.plot(testY,label='test data')
plt.plot(testPredict,label='Predict')
plt.legend()
plt.show() 

#save plot to 'png'file
now=datetime.now()
date=''+str(now.year)+'-'+str(now.month)+'-'+str(now.day)+'T'+str(now.hour)+str(now.minute)

fig.savefig('plot\RMSE'+str(testScore)+'_lookback3LSTM16Dense1LR05epoch500.png')

# predict last value (or tomorrow?)
lastX = testX[-1]

for i in range(output_size):
    lastX = np.reshape(lastX, (1, 1, look_back))
    print(lastX)
    lastY = model.predict(lastX)
    
    for j in range(0,look_back):
        if(j>=(look_back-1)):
            lastX[0][0][j]=lastY
        else:
            lastX[0][0][j] = lastX[0][0][j+1]

    lastY = scaler.inverse_transform(lastY)
    print('Predict the Close value of final day=: %f' %lastY)  # 데이터 입력 마지막 다음날 종가 예측

#save model
from keras.models import load_model
model.save('mnist_mlp_model_1.h5')
