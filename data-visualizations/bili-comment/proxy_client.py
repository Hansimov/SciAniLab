import os
import sys
import socket
import datetime
import pickle

host = "127.0.0.1"
port = 23333
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

msg = "client connected at {}".format(datetime.datetime.now())

sock.connect((host,port))

print("+ Connected {}:{}!".format(host,port))

sock.send(msg.encode())
data = pickle.loads(sock.recv(1024))
print(*data)

sock.close()