import os
import sys
import socket

host = "127.0.0.1"
port = 23333
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
msg_L = ["this is client"]
msg = msg_L.extend(sys.argv[1:])
sock.connect((host,port))
print("+ Connected {}:{}!".format(host,port))

for msg in msg_L:
    sock.send(msg.encode())
    print(sock.recv(1024).decode())
sock.close()
