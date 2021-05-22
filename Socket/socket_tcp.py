from socket import *
from os.path import exists
import sys
import re
import math
from matplotlib import pyplot as plt
from matplotlib import animation
import time
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers
from keras.models import load_model
from random import *
import math

ts = 200
list_rand = []
for i in range(0, 200):
    list_rand.append(round(uniform(0, 200), 2))
model = load_model('phm_model2.h5')
df = pd.Series(list_rand, dtype = np.float64)
N=df.size
mean = df.mean()
std = np.std(df)
df = df.map(lambda x : (x - mean) / std) # 정규화
print(len(df))
    #model = load_model('phm_model2.h5')

df_new=df[-ts:]
df_new = np.asarray([np.array([df.values[i+j] for j in range(ts)])
            for i in range(len(df_new) - ts+1)]).reshape(-1,ts,1) 

print("예측 시작")
for i in range(0, ts):
    pred = model.predict(df_new)
    print(i)
    for j in range(0, df_new.size-1):
            df_new[-1][j]=df_new[-1][j+1]
    df_new[-1][-1]=pred
print("예측 완료")

serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('', 8080))
serverSock.listen(1)

ts = 200
while(1) :
    a = ""
    df = pd.Series()
    connectionSock, addr = serverSock.accept()
    data = connectionSock.recv(4096)
    print('받은 데이터 : ', data.decode('utf-8'))
    a = data.decode('utf-8')
    a = a.strip()
    a = re.split('[ \[| \] |, | ]', a)
    a = ' '.join(a).split()
    list_a = []
    list_a = list(map(float, a))
    print(len(list_a))
    df = pd.Series(list_a, dtype = np.float64)
    N=df.size
    mean = df.mean()
    std = np.std(df)
    df = df.map(lambda x : (x - mean) / std) # 정규화
    print(len(df))
    #model = load_model('phm_model2.h5')

    df_new=df[-ts:]
    df_new = np.asarray([np.array([df.values[i+j] for j in range(ts)])
                for i in range(len(df_new) - ts+1)]).reshape(-1,ts,1) 

    print("예측 시작")
    for i in range(0, ts):
        pred = model.predict(df_new)
        print(i)
        for j in range(0, df_new.size-1):
                df_new[-1][j]=df_new[-1][j+1]
        df_new[-1][-1]=pred
    print("예측 완료")
            
    #print(df_new[-1])
    df_new[-1] = df_new[-1] * std + mean
    df_new[-1] = np.round(df_new[-1], 2)
    print("전송중")
    connectionSock.send(str(df_new[-1]).encode('utf-8'))
    print("전송완료")
    print(df_new[-1])
    print(len(df_new[-1]))
    connectionSock.close()