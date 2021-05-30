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
error_count=0 # 전류 예측 에러
error_check=0 # 전류 예측 에러 (체크)
v_error_check_pred=0 # 전압 예측 에러

e_error_check_real=0 # 전류 실시간 에러
v_error_check_real=0
s_error_check_real=0
t_error_check_real=0
sound_error_count=0
voltage_error_count=0

select=0 # 현재 선택된 상태 (전류 or 전압)
datatype=0 # 보낸 데이터의 종류, 들어올 데이터의 종류( 전류 or 전압 )

last_time =""   # last update
def Recv():
    clientSock = socket(AF_INET, SOCK_STREAM)
    clientSock.connect(('172.30.1.22', 8080))
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
    global error_count
    global datatype
    global v_error_check_pred
    global y_pred_ticks
    if(datatype==0):
        ax_7.cla()
        ax_7.axis([0,200,-20,60])
        y_pred_ticks= np.arange(-20, 61, 10)
        ax_7.set_yticks(y_pred_ticks)
        X=np.array(range(0,ts))
        ax_7.plot(X,np.array(a),'r-')
        ax_7.grid(True,alpha=0.3)
        fig2.suptitle("Predicted Electric Current")
        for i in a:
            if i >=30:
                error_count+=1
    
    ave=0
    if(datatype==1):
        ax_7.cla()
        ax_7.axis([0,200,480,520])
        y_pred_ticks= np.arange(480, 521, 5)
        ax_7.set_yticks(y_pred_ticks)
        X=np.array(range(0,ts))
        ax_7.plot(X,np.array(a),'k-')
        ax_7.grid(True,alpha=0.3)
        fig2.suptitle("Predicted Voltage")
        if np.mean(a) >=499 :
            v_error_check_pred=1
    
    now = datetime.datetime.now()
    global last_time
    last_time = now.strftime("%Y-%m-%d_%H:%M:%S")
    clientSock.close()

  

thread1 = threading.Thread(target=Recv)

l = []
y=[0,0,0,0,0]
count=0 # csv 인덱스
ts = 200 
recv = 0

fig = plt.figure(figsize = (8,4))
plt.suptitle("Real-time Data")
fig2 = plt.figure(figsize = (8,2))
plt.suptitle("Predicted Data")
gs  = GridSpec(nrows=2,ncols=2)
gs2 = GridSpec(nrows=1,ncols=1)

#x_ticks = np.arange(0, 21, 2)
x_ticks = np.arange(0, 101, 10)
x_pred_ticks= np.arange(0, 201, 10)

y_ticks1 = np.arange(0, 31, 5)
y_ticks2 = np.arange(0, 41, 5)
y_ticks3 = np.arange(-20, 61, 10)
y_ticks4 = np.arange(480, 521, 5)
y_pred_ticks= np.arange(-20, 61, 10)

ax = fig.add_subplot(gs[0,0], xlim=(0, 100), ylim=(0, 30)) # [0,0]에 그림
max_points = 100
line, = ax.plot(np.arange(max_points), np.ones(max_points, dtype=np.float)*np.nan, lw=1, c='blue',ms=1)
ax.set_title("Sounds",fontsize =12)
ax.set_xticks(x_ticks)
ax.set_yticks(y_ticks1)
ax.grid(True,alpha=0.3)

ax_2 = fig.add_subplot(gs[0,1], xlim=(0, 100), ylim=(0, 40))
max_points_2 = 100
line_2, = ax_2.plot(np.arange(max_points_2), np.ones(max_points_2, dtype=np.float)*np.nan, lw=1, c='green',ms=1)
ax_2.set_title("Temperature",fontsize =12)
ax_2.set_xticks(x_ticks)
ax_2.set_yticks(y_ticks2)
ax_2.grid(True,alpha=0.3)

ax_3 = fig.add_subplot(gs[1,0], xlim=(0, 100), ylim=(-20, 60))
max_points_3 = 100
line_3, = ax_3.plot(np.arange(max_points_3), np.ones(max_points_3, dtype=np.float)*np.nan, lw=1, c='red',ms=1)
ax_3.set_title("Electric Current",fontsize =12)
ax_3.set_xticks(x_ticks)
ax_3.set_yticks(y_ticks3)
ax_3.grid(True,alpha=0.3)


ax_4 = fig.add_subplot(gs[1,1], xlim=(0, 100), ylim=(480, 520))
max_points_4 = 100
line_4, = ax_4.plot(np.arange(max_points_4), np.ones(max_points_4, dtype=np.float)*np.nan, lw=1, c='black',ms=1)
ax_4.set_title("Voltage",fontsize =12)
ax_4.set_xticks(x_ticks)
ax_4.set_yticks(y_ticks4)
ax_4.grid(True,alpha=0.3)

fig.tight_layout()

ax_7 = fig2.add_subplot(gs2[0,0], xlim=(0, 200), ylim=(-20, 60))
max_points_3 = 100
ax_7.set_xticks(x_pred_ticks)
ax_7.set_yticks(y_pred_ticks)
ax_7.grid(True,alpha=0.3)

fig2.tight_layout()

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
    global select
    global datatype
    global v_error_check_pred
    global e_error_check_real
    global v_error_check_real
    global s_error_check_real
    global t_error_check_real
    global sound_error_count
    global voltage_error_count

    if len(LINE)==4:
        l.append(LINE) # 리스트 추가
        if int(LINE[1]) >=50:
            t_error_check_real+=1
        if int(LINE[2]) >=40:
            e_error_check_real+=1
        if int(LINE[0]) <=15:
            sound_error_count+=1
        if int(LINE[3]) >=500:
            voltage_error_count+=1

    df_csv = pd.DataFrame(l, columns=['Sounds', 'Temperature','Electric Current','Voltage'])
    df_csv.to_csv('sensor_data.csv', index=True, encoding='cp949')  # csv 생성
    count+=1

    if count==205:
        # 소리 에러 갯수 확인
        if sound_error_count >=140:
            s_error_check_real=1

        # 전압 에러 갯수 확인
        if voltage_error_count >=100:
            v_error_check_real=1

        # 선택 상태 확인
        if select==0:
            col_list = ['Electric Current']
            datatype=0
        elif select==1:
            col_list = ['Voltage']
            datatype=1

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

    table()
    temp = "Voltage  : %2d    Electric Current : %2d    Sound : %2d   Temp : %2d "% (y[3],y[2],y[0],y[1])
    label.config(text=temp)

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

    global error_count
    global error_check
    global v_error_check_pred
    global e_error_check_real
    global v_error_check_real
    global s_error_check_real
    global t_error_check_real

    
    # 전류 예측 에러 검사
    if error_count >= 10 :
        if(error_check == 0):
            error_check+=1
            Alarm()
            scrt.insert(Tk.INSERT, "E.C\n", 'error')
            scrt.tag_config('error', foreground='red')
            
    # 전압 예측 에러 검사
    if v_error_check_pred == 1:
        v_error_check_pred+=1
        Alarm()
        scrt.insert(Tk.INSERT, "Voltage\n", 'error')
        scrt.tag_config('error', foreground='red')

    # 온도 실시간 에러 검사
    if t_error_check_real == 1:
        t_error_check_real+=1
        ax_2.set_facecolor('tomato')
    # 전류 실시간 에러 검사
    if e_error_check_real == 1:
        e_error_check_real+=1
        ax_3.set_facecolor('tomato')
    # 소리 실시간 에러 검사
    if s_error_check_real == 1:
        s_error_check_real+=1
        ax.set_facecolor('tomato')
    # 전압 실시간 에러 검사
    if v_error_check_real == 1:
        v_error_check_real+=1
        ax_4.set_facecolor('tomato')


    return line_4 

root = Tk.Tk() #추가 
root.title("PHM")
root.geometry("1300x800+120+50")
root.resizable(False,False)
root.configure(bg='white')


# 수리,점검 버튼 이벤트
def btncmd():
    global error_check
    global error_count
    global v_error_check_pred
    global e_error_check_real
    global v_error_check_real
    global s_error_check_real
    global t_error_check_real

    if(combobox.get() == "Voltage_Predict"):  # 값 설정       
        Alarm()
        scrt.insert(Tk.INSERT," V repair\n")       
        ax_3.set_facecolor('white')
        v_error_check_pred=0
    elif(combobox.get() == "Electric Current_Predict"):
        Alarm()
        scrt.insert(Tk.INSERT," E.C repair\n")
        ax_3.set_facecolor('white')
        error_check=0
        error_count=0

    elif(combobox.get() == "Temperature"):       
        ax_2.set_facecolor('white')
        t_error_check_real=0
    elif(combobox.get() == "Electric Current_Real"):
        ax_3.set_facecolor('white')
        e_error_check_real=0
    elif(combobox.get() == "Sounds"):
        ax.set_facecolor('white')
        s_error_check_real=0
    elif(combobox.get() == "Voltage_Real"):
        ax_4.set_facecolor('white')
        v_error_check_real=0

##경과시간
start_time = time.time()
def elapsedTime():

    elapsed_time = time.time() - start_time
    m, s = divmod(elapsed_time, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    
    if d > 0:
        dtime = str(int(d)) + "d_"
    else: 
        dtime = ""
        
    if h > 0:
        htime = str(int(h)) + ":"
    else:
        htime = "00:"
        
    if m > 0:
        mtime = str(int(m)) + ":"
    else:
        mtime = "00:"
    
        
    strTime = dtime+"%02d:%02d:%02d" % (h,m,s)
    return strTime 

def Alarm():
    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S ')
    scrt.insert(Tk.INSERT, nowDatetime)

def choose():
     global select

     if(combobox2.get() == "Voltage"):
         select = 1
     elif(combobox2.get() == "Electric Current"):
         select = 0

         
def table():
    Detail.insert('',2,text="Runtime",values=elapsedTime())
    Detail.insert('',3,text="Last Update",values=last_time)

scrt = tkst.ScrolledText(root, width=50, height=25)
scrt.grid(row = 1,column = 1)


values = ["Voltage_Predict","Voltage_Real","Electric Current_Predict","Electric Current_Real","Sounds", "Temperature"]

combobox = ttk.Combobox(root,height=5,values=values)
combobox.grid(row = 3,column = 1)
combobox.set("선택")

btn = Tk.Button(root, text = "점검",command = btncmd)
btn.grid(row = 5,column = 1)

values2 = ["Voltage","Electric Current"]

combobox2 = ttk.Combobox(root,height=5,values=values2)
combobox2.grid(row = 3,column = 0)
combobox2.set("Electric Current")

btn2 = Tk.Button(root, text = "확인", command = choose)
btn2.grid(row = 5,column = 0)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=0,row=1) 

canvas2 = FigureCanvasTkAgg(fig2, master=root)
canvas2.get_tk_widget().grid(column=0,row=2) 

## 시간 , 데이터

now = datetime.datetime.now()
s = now.strftime("%Y-%m-%d %H:%M:%S")
t = now.strftime("%Y-%m-%d_%H:%M:%S")


temp = "Voltage  : 0    Electric Current : 0    Sound : 0   Temp : 0 "
label = ttk.Label(root, text=temp,padding =(40,10), font=("Bahnschrift SemiBold","16"),background = "white", relief ="solid")
label.grid(row = 0,column=0)

empty_label = ttk.Label(root,text="",font = ("","3"),background = "white")
empty_label.grid(row=4,column=0)

empty_label2 = ttk.Label(root,text="",font = ("","3"),background = "white")
empty_label2.grid(row=4,column=1)

## 표

Detail = ttk.Treeview(root,columns=["one"],displaycolumns=["one"],height=4)
Detail.grid(row=2,column=1)

Detail.column("#0", width=200,anchor="s")
Detail.heading("#0", text="Data",anchor="s")
 
Detail.column("#1", width=200)
Detail.heading("#1", text="Value", anchor="center")

Detail.insert('',0,text="Start Time",values=t)
Detail.insert('',1,text="Updates/sec",values="40")
Detail.insert('',2,text="Runtime",values=elapsedTime())
Detail.insert('',3,text="Last Update",values ="::")
 

anim = animation.FuncAnimation(fig, animate  , init_func= init ,frames=200, interval=50, blit=False)
anim_2 = animation.FuncAnimation(fig, animate_2 ,init_func= init_2 ,frames=200, interval=50, blit=False)
anim_3 = animation.FuncAnimation(fig, animate_3 ,init_func= init_3 ,frames=200, interval=50, blit=False)
anim_4 = animation.FuncAnimation(fig2, animate_4 ,init_func= init_4 ,frames=200, interval=50, blit=False)


Tk.mainloop()
