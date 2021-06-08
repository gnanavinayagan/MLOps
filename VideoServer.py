#!/usr/bin/env python
# coding: utf-8
import socket, cv2, pickle,struct
from threading import Thread

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Socket created")

port = 22222 # i'm 22222. for sending use this
s.bind(('',port))
print("socket binded to %s " %(port))
s.listen()

data = b""
payload_size = struct.calcsize("Q")


def send(csessiona, addr):

    to_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_ip = addr[0] # paste your server ip address here
    port = 33333
    to_socket.connect((host_ip,port)) # a tuple
    if to_socket:
        vid = cv2.VideoCapture(0)

        while(vid.isOpened()):
            img,frame = vid.read()
            frame = frame[100:700,100:700]
            a = pickle.dumps(frame)
            message = struct.pack("Q",len(a))+a
            to_socket.sendall(message)
            


csessiona, addr = s.accept()
print('GOT CONNECTION FROM:',addr)
t1 = Thread(target=send,args=(csessiona,addr))
t1.start()



#receiving 
data = b""
payload_size = struct.calcsize("Q")
while True:
    while len(data) < payload_size:
        packet = csessiona.recv(4*1024) # 4K
        if not packet: break
        data+=packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q",packed_msg_size)[0]
    
    while len(data) < msg_size:
        data += csessiona.recv(4*1024)
    frame_data = data[:msg_size]
    data  = data[msg_size:]
    frame = pickle.loads(frame_data)
    cv2.imshow("I'm server: Client's VIDEO",frame)
    key = cv2.waitKey(1) & 0xFF
    if key  == ord('q'):
        break



csessiona.close()
    


# In[ ]:




