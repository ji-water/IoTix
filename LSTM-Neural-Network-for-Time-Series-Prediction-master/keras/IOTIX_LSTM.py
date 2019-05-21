"""https://tbacking.com/2017/08/18/%EC%88%9C%ED%99%98-%EC%8B%A0%EA%B2%BD%EB%A7%9D-lstm-%ED%99%9C%EC%9A%A9-%EC%A3%BC%EA%B0%80-%EC%98%88%EC%B8%A1/"""

import os
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import math
from sklearn.metrics import mean_squared_error
from datetime import datetime
 
look_back = 1
def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i + look_back)]
        dataX.append(a)
        dataY.append(dataset[i + look_back])
    return np.array(dataX), np.array(dataY)
 
# file loader
#sydtpath = "D:sydt"
#naturalEndoTekCode = "A168330"
#fullpath = sydtpath + os.path.sep + naturalEndoTekCode + '.csv'
pandf = pd.read_csv('testdata4.csv')
 

now=datetime.now()
date=''+str(now.year)+'-'+str(now.month)+'-'+str(now.day)+'T'+str(now.hour)+str(now.minute)
print(date)


# convert nparray
nparr = pandf['length'].values[:] #순서대로 , q반대는 [::-1]
nparr.astype('float32')
print(nparr)
 
# normalization
nparr = nparr.reshape(-1,1)
scaler = MinMaxScaler(feature_range=(0, 1))
nptf = scaler.fit_transform(nparr)
print(nptf)

# split train, test
train_size = int(len(nptf) * 0.9)
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
model.add(LSTM(4, input_shape=(1, look_back)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(trainX, trainY, epochs=10, batch_size=1, verbose=2)
 
# make prediction
testPredict = model.predict(testX)
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform(testY)
testScore = math.sqrt(mean_squared_error(testY, testPredict))
print('Train Score: %.2f RMSE' % testScore)
 
# predict last value (or tomorrow?)
lastX = nptf[-1]
lastX = np.reshape(lastX, (1, 1, 1))
lastY = model.predict(lastX)
lastY = scaler.inverse_transform(lastY)
print('Predict the Close value of final day: %d' % lastY)  # 데이터 입력 마지막 다음날 종가 예측
 
# plot
fig = plt.figure(facecolor='white')
ax = fig.add_subplot(111) 
ax.plot(testY, label='True Data')
plt.plot(testPredict, label='Prediction')
plt.legend()
plt.show()

#save plot to 'png'file
now=datetime.now()
date=''+str(now.year)+'-'+str(now.month)+'-'+str(now.day)+'T'+str(now.hour)+str(now.minute)
fig.savefig('plot\ '+date+'.png')