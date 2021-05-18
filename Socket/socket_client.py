from socket import *
from random import *
import math
import re
import threading
import time
global recv
recv = 0

def Recv(clientSock):
    while True:
        global recv
        list_recv = clientSock.recv(2048)
        a = list_recv.decode('utf-8')
        a = a.strip()
        a = re.split('[ \[| \] |, | ]', a)
        a = ' '.join(a).split()
        a = list(map(float, a))
        print(a) # a를 list 형태로 변환
        recv = 1
        break;

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('127.0.0.1', 8080))

print("연결 완료\n")

list_rand = []
for i in range(0, 200):
    list_rand.append(round(uniform(0, 200), 2))


### if count = 200 :
list_rand = str(list_rand)
clientSock.send(list_rand.encode())
print("전송 완료\n")
thread1 = threading.Thread(target=Recv, args = (clientSock, ))
thread1.start()
count = 0
while(recv != 1):
    count += 1
    print(count)
    time.sleep(1)

