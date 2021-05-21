# * [译]Python 中的 Socket 编程（指南） 
# ** https://keelii.com/2018/09/24/socket-programming-in-python/

# * python socket编程 - 刘江的python教程 
# ** https://www.liujiangblog.com/course/python/76

# * 套接字编程指南 — Python 3.8.2 文档 
# ** https://docs.python.org/zh-cn/3/howto/sockets.html


import os
import sys
import socket

host = "127.0.0.1"
port = 23333

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((host,port))
server_sock.listen()

conn, addr = server_sock.accept()

print("> Monitoring {}:{} ...".format(host,port))

while True:
    data = conn.recv(1024)
    if not data:
        print("x Client disconnected!")
        break
    else:
        print("= Message from client: {}".format(data.decode()))
        conn.send("message from server".format(data.decode()).encode())

# conn.close()