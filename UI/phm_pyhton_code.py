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

PORT = 'COM5' # 포트 번호
BaudRate = 9600 # 전송 속도
ARD = Serial(PORT,BaudRate) # 아두이노와 연결되는 통신 시리얼 객체
l = []

fig = plt.figure(figsize = (11.4, 3))     #figure(도표) 생성

ax = plt.subplot(311, xlim=(0, 100), ylim=(30, 75))

max_points = 100

line, = ax.plot(np.arange(max_points), np.ones(max_points, dtype=np.float)*np.nan, lw=1, c='blue',ms=1)

def init():
    return line

def animate(i):
    LINE= ARD.readline()
    LINE = LINE.decode('utf-8')[:len(LINE)-2]
    if LINE[0]=='M':
        LINE = LINE.replace("M","")
        LINE = LINE.split(',')
        y = float(LINE[0]) # for문으로 변수 여러개
        y = int(LINE[0])
        y = int(y)
        old_y = line.get_ydata()
        new_y = np.r_[old_y[1:], y]
        line.set_ydata(new_y)
        ARD.flushInput()

    print(LINE)
    l.append(LINE) # 리스트 추가
    df = pd.DataFrame(l, columns=['Humidity', 'Temperature'])
    df.to_csv('sensor_data.csv', index=False, encoding='cp949')  # csv 생성
    return line,


root = Tk.Tk() #추가
root.geometry("1080x540+450+350")
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=0,row=1) 

anim = animation.FuncAnimation(fig, animate  , init_func= init ,frames=50, interval=50, blit=False)

Tk.mainloop()