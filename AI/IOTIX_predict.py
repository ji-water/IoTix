# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 18:55:59 2019

@author: bjiso
"""

import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import math
from sklearn.metrics import mean_squared_error
from datetime import datetime
import json
from pprint import pprint

look_back = 3 #input size
output_size = 7 #predict time 7

###### 1. DATASET #######

with open('sample_predict.json') as json_file:
    json_data = json.load(json_file)   
print("file open")

arr=[]
for i in range(0, look_back):
    arr.append(float(json_data['test'][i]['length']))
    
print(arr)
nparr=np.array(arr)
nparr.astype('float32')
nparr = nparr.reshape(-1,1)
scaler = MinMaxScaler(feature_range=(0, 1))
nptf = scaler.fit_transform(nparr)

testX = []
for i in range(look_back):
    testX.append(nptf[i])
testX = np.array(testX)
testX = np.reshape(testX, (1,1,look_back))
print(testX)
print(testX.shape)

####### 2. LOAD MODEL #######
from keras.models import load_model
model = load_model('mnist_mlp_model_2.h5')

predictY = []
####### 3. PREDICT #######
for i in range(output_size):
    testX = np.reshape(testX, (1,1,look_back))
    testY = model.predict(testX)
    
    for j in range(0,look_back):
        if(j>=(look_back-1)):
            testX[0][0][j]=testY
        else:
            testX[0][0][j] = testX[0][0][j+1]
            
    testY = scaler.inverse_transform(testY)
    predictY.append(testY[0][0].tolist())

pprint('Predict the Close value of final day : {}'.format(predictY))
