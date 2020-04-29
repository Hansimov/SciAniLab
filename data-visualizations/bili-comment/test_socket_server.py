import os
import sys
import socket

host = "127.0.0.1"
port = 23333

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host,port))
sock.listen()

conn, addr = sock.accept()

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