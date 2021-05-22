from serial import Serial
import tkinter as Tk
from matplotlib import pyplot as plt
from matplotlib import animation
import random
import time
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
from matplotlib.gridspec import GridSpec
import tkinter.ttk as ttk
import tensorflow as tf
from tensorflow.keras import layers
from keras.models import load_model
import tkinter.scrolledtext as tkst
import datetime
from socket import *
import math
import re
import threading



PORT = 'COM5' # 포트 번호
BaudRate = 9600 # 전송 속도
ARD = Serial(PORT,BaudRate) # 아두이노와 연결되는 통신 시리얼 객체
list_df=""


def Recv():
    clientSock = socket(AF_INET, SOCK_STREAM)
    clientSock.connect(('172.30.1.45', 8080))
    print(list_df)
    clientSock.send(list_df.encode())
    print("전송 완료\n")

    list_recv = clientSock.recv(4096)
    a = list_recv.decode('utf-8')
    a = a.strip()
    a = re.split('[ \[| \] |, | ]', a)
    a = ' '.join(a).split()
    a = list(map(float, a))
    print(a) # a를 list 형태로 변환
    recv = 1

    global ax_7
    ax_7.cla()
    ax_7.axis([0,100,-20,50])
    X=np.array(range(0,ts))
    ax_7.plot(X,np.array(a),'r-')
    clientSock.close()

  

thread1 = threading.Thread(target=Recv)

l = []
y=[0,0,0,0,0]
count=0 # csv 인덱스
ts = 200 
recv = 0

fig = plt.figure(figsize = (4,4))
plt.suptitle("Real-time Data")
fig2 = plt.figure(figsize = (8,4))
plt.suptitle("     Real-time Data                                       Predicted Data")
gs  = GridSpec(nrows=2,ncols=1)
gs2 = GridSpec(nrows=2,ncols=2)

ax = fig.add_subplot(gs[0,0], xlim=(0, 100), ylim=(0, 80)) # [0,0]에 그림
max_points = 100
line, = ax.plot(np.arange(max_points), np.ones(max_points, dtype=np.float)*np.nan, lw=1, c='blue',ms=1)
ax.get_xaxis().set_visible(False) # x축 제거
ax.set_title("Sounds",fontsize =9)

ax_2 = fig.add_subplot(gs[1,0], xlim=(0, 100), ylim=(0, 40))
max_points_2 = 100
line_2, = ax_2.plot(np.arange(max_points_2), np.ones(max_points_2, dtype=np.float)*np.nan, lw=1, c='green',ms=1)
ax_2.get_xaxis().set_visible(False) # x축 제거
ax_2.set_title("Temperature",fontsize =9)


ax_3 = fig2.add_subplot(gs2[0,0], xlim=(0, 100), ylim=(-20, 50))
max_points_3 = 100
line_3, = ax_3.plot(np.arange(max_points_3), np.ones(max_points_3, dtype=np.float)*np.nan, lw=1, c='red',ms=1)
ax_3.get_xaxis().set_visible(False) # x축 제거
ax_3.set_title("Electric Current",fontsize =9)


ax_4 = fig2.add_subplot(gs2[1,0], xlim=(0, 100), ylim=(480, 520))
max_points_4 = 100
line_4, = ax_4.plot(np.arange(max_points_4), np.ones(max_points_4, dtype=np.float)*np.nan, lw=1, c='black',ms=1)
ax_4.get_xaxis().set_visible(False) # x축 제거
ax_4.set_title("Voltage",fontsize =9)


ax_7 = fig2.add_subplot(gs2[0,1], xlim=(0, 100), ylim=(-20, 50))
max_points_3 = 100
ax_7.get_xaxis().set_visible(False) # x축 제거
ax_7.set_title("Predicted Electric Current",fontsize =9)

ax_8 = fig2.add_subplot(gs2[1,1], xlim=(0, 100), ylim=(-20, 50))
max_points_3 = 100
ax_8.get_xaxis().set_visible(False) # x축 제거
ax_8.set_title("Predicted Voltage",fontsize =9)

#################################
def init():
    return line

def init_2():
    return line_2

def init_3(): 
    return line_3

def init_4():
    return line_4



def animate(i):
    global y
    LINE= ARD.readline()
    LINE = LINE.decode('utf-8')[:len(LINE)-2]
    if LINE[0]=='M':
        LINE = LINE.replace("M","")
        LINE = LINE.split(',')
        for i in range(0,4):
            y[i] = float(LINE[i]) # for문으로 변수 여러개
            y[i] = int(LINE[i])
            y[i] = int(y[i])
        
        old_y = line.get_ydata()
        new_y = np.r_[old_y[1:], y[0]]
        line.set_ydata(new_y)
        ARD.flushInput()

    global count
    global flag
    global ts

    if len(LINE)==4:
        l.append(LINE) # 리스트 추가
    df_csv = pd.DataFrame(l, columns=['Sounds', 'Temperature','Electric Current','Voltage'])
    df_csv.to_csv('sensor_data.csv', index=True, encoding='cp949')  # csv 생성
    count+=1

    if count==205:
        col_list = ['Electric Current']
        dataframe = pd.read_csv('sensor_data.csv', usecols=col_list)
        df = np.array(dataframe).flatten()
        df = df.tolist()
        df = df[-ts:]
        ####
        global list_df
        list_df = str(df)
        thread1 = threading.Thread(target=Recv)
        thread1.start()
          
        #####
        count=0

    return line,

def animate_2(i):   
    old_y = line_2.get_ydata()
    new_y = np.r_[old_y[1:], y[1]]
    line_2.set_ydata(new_y)

    return line_2  

def animate_3(i):   
    old_y = line_3.get_ydata()
    new_y = np.r_[old_y[1:], y[2]]
    line_3.set_ydata(new_y)

    return line_3 

def animate_4(i):   
    old_y = line_4.get_ydata()
    new_y = np.r_[old_y[1:], y[3]]
    line_4.set_ydata(new_y)

    return line_4 

root = Tk.Tk() #추가 
root.title("PHM")
root.geometry("1500x620+120+50")
root.resizable(False,False)
root.configure(bg='white')


def btncmd():
    if(combobox.get() == "Voltage"):  # 값 설정       
        Alarm()
        scrt.insert(Tk.INSERT," V repair\n")
    elif(combobox.get() == "Electric Current"):
        Alarm()
        scrt.insert(Tk.INSERT," E.C repair\n")


def Alarm():
    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S ')
    scrt.insert(Tk.INSERT, nowDatetime)


scrt = tkst.ScrolledText(root, width=33, height=5)
scrt.grid(row = 1,column = 0)
ttk.Label(root, text="Time").grid(column=0,row=2) 


values = ["Voltage","Electric Current","temperature"]

combobox = ttk.Combobox(root,height=5,values=values)
combobox.grid(row = 1,column = 1)
combobox.set("선택")

btn = Tk.Button(root, text = "수리",command = btncmd)
btn.grid(row = 2,column = 1)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=0,row=0) 

canvas2 = FigureCanvasTkAgg(fig2, master=root)
canvas2.get_tk_widget().grid(column=1,row=0) 

anim = animation.FuncAnimation(fig, animate  , init_func= init ,frames=200, interval=50, blit=False)
anim_2 = animation.FuncAnimation(fig, animate_2 ,init_func= init_2 ,frames=200, interval=50, blit=False)
anim_3 = animation.FuncAnimation(fig2, animate_3 ,init_func= init_3 ,frames=200, interval=50, blit=False)
anim_4 = animation.FuncAnimation(fig2, animate_4 ,init_func= init_4 ,frames=200, interval=50, blit=False)

Tk.mainloop()
