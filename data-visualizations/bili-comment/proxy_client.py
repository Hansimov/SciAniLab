import os
import sys
import socket
import datetime
import pickle

host = "127.0.0.1"
port = 23333
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# msg = "client connected at {}".format(datetime.datetime.now())
# msg = ["get",[]]
# msg = ["del",[]]

sock.connect((host,port))

# print("+ Connected {}:{}!".format(host,port))

# sock.send(msg.encode())
proxy = ["get",[]]
# proxy = ["del", ["180.252.181.2","80","http"]]
proxy_pkl = pickle.dumps(proxy)
sock.sendall(proxy_pkl)
if proxy[0]=="get":
    data = pickle.loads(sock.recv(1024))
    print(*data)

sock.close()