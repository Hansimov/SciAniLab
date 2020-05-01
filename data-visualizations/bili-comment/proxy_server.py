import os
import sys
import time
import socket
import pickle

# fetch proxies in advance
# if a proxy in client is invalid, then the client requests for a new proxy
# server returns a valid proxy when receiving a client request

def select_proxy(conn):
    proxy = ["123.123.123.123","12345","https"]
    proxy_pkl = pickle.dumps(proxy)
    conn.sendall(proxy_pkl)
    print("Sending {:<15} {:<5} {:<5}".format(*proxy[:3]))


def run_server(timeout=2):
    host = "127.0.0.1"
    port = 23333

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host,port))
    sock.listen()
    sock.settimeout(timeout)
    print("> Listening {}:{} ...".format(host,port))

    try:
        while True:
            try:
                conn, addr = sock.accept()
                data = conn.recv(1024)
                if not data:
                    print("x Client disconnected!")
                    break
                else:
                    # print("> Message from client: {}".format(data.decode()))
                    # msg = "> Message from server".format(data.decode()).encode()
                    # conn.sendall(msg)
                    select_proxy(conn)
            except socket.timeout:
                print("Timeout")
            except KeyboardInterrupt:
                pass
    except KeyboardInterrupt:
        print("Server closed with KeyboardInterrupt!")


if __name__ == '__main__':
    run_server(2)

