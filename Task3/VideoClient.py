import socket,cv2, pickle,struct
from threading import Thread

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Socket created")

port = 33333 # i'm 22222. for sending use this
s.bind(('',port))
print("socket binded to %s " %(port))
s.listen()



def send():


    to_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_ip = "192.168.0.105" # paste your server ip address here
    port = 22222
    to_socket.connect((host_ip,port)) # a tuple
    if to_socket:
        vid = cv2.VideoCapture(0)

        while(vid.isOpened()):
            img,frame = vid.read()
            frame = frame[500:700,500:700]
            a = pickle.dumps(frame)
            message = struct.pack("Q",len(a))+a
            to_socket.sendall(message)
            




t1 = Thread(target=send)
t1.start()

csessiona, addr = s.accept()
print('GOT CONNECTION FROM:',addr)



# create socket # receiving part
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
    cv2.imshow("I'm Client: Server's VIDEO",frame)
    key = cv2.waitKey(1) & 0xFF
    if key  == ord('q'):
        break



csessiona.close()
