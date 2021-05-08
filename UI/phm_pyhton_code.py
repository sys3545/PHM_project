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


PORT = 'COM5' # 포트 번호
BaudRate = 9600 # 전송 속도
ARD = Serial(PORT,BaudRate) # 아두이노와 연결되는 통신 시리얼 객체
l = []
y=[0,0,0,0,0]
count=0 # csv 인덱스

fig = plt.figure(figsize = (8,6))
gs  = GridSpec(nrows=4,ncols=2)


ax = fig.add_subplot(gs[0,0], xlim=(0, 100), ylim=(0, 40)) # [0,0]에 그림
max_points = 100
line, = ax.plot(np.arange(max_points), np.ones(max_points, dtype=np.float)*np.nan, lw=1, c='blue',ms=1)
ax.get_xaxis().set_visible(False) # x축 제거
ax.set_title("Sounds",fontsize =9)

ax_2 = fig.add_subplot(gs[1,0], xlim=(0, 100), ylim=(0, 40))
max_points_2 = 100
line_2, = ax_2.plot(np.arange(max_points_2), np.ones(max_points_2, dtype=np.float)*np.nan, lw=1, c='green',ms=1)
ax_2.get_xaxis().set_visible(False) # x축 제거
ax_2.set_title("Vibration",fontsize =9)


ax_3 = fig.add_subplot(gs[2,0], xlim=(0, 100), ylim=(-20, 50))
max_points_3 = 100
line_3, = ax_3.plot(np.arange(max_points_3), np.ones(max_points_3, dtype=np.float)*np.nan, lw=1, c='red',ms=1)
ax_3.get_xaxis().set_visible(False) # x축 제거
ax_3.set_title("Electric Current",fontsize =9)


ax_4 = fig.add_subplot(gs[3,0], xlim=(0, 100), ylim=(480, 520))
max_points_4 = 100
line_4, = ax_4.plot(np.arange(max_points_4), np.ones(max_points_4, dtype=np.float)*np.nan, lw=1, c='black',ms=1)
ax_4.get_xaxis().set_visible(False) # x축 제거
ax_4.set_title("Voltage",fontsize =9)


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

    print(LINE)
    global count;
    l.append(LINE) # 리스트 추가
    df = pd.DataFrame(l, columns=['Sounds', 'vibration','Electric Current','Voltage'])
    #df = pd.DataFrame.from_dict([{'Sounds':LINE[0],'vibration':LINE[1],'Electric Current':LINE[2],'Voltage':LINE[3]}])
    #df = pd.DataFrame({'Sounds':LINE[0],'vibration':LINE[1],'Electric Current':LINE[2],'Voltage':LINE[3]}, index=[count])
    count+=1
    df.to_csv('sensor_data.csv', index=True, encoding='cp949')  # csv 생성
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
root.geometry("1080x700+450+350")
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=0,row=1) 

anim = animation.FuncAnimation(fig, animate  , init_func= init ,frames=200, interval=50, blit=False)
anim_2 = animation.FuncAnimation(fig, animate_2 ,init_func= init_2 ,frames=200, interval=50, blit=False)
anim_3 = animation.FuncAnimation(fig, animate_3 ,init_func= init_3 ,frames=200, interval=50, blit=False)
anim_4 = animation.FuncAnimation(fig, animate_4 ,init_func= init_4 ,frames=200, interval=50, blit=False)

Tk.mainloop()
