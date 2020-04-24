import os
import subprocess
import requests
import socket
import json

# ip, port, kind = "117.88.176.162", "3000", "https"
ip, port, kind = "124.156.98.172", "80", "http"

url = "{}://api.bilibili.com/x/v2/reply?pn=1&type=1&oid=667592495&sort=2&_=1587689751023"

http_D = {
    "http":  "http://{}:{}".format(ip,port),
    "https": "https://{}:{}".format(ip,port),
    "ftp":   "ftp://{}:{}".format(ip,port)
}

headers = {
    "user-agent": "my-app/0.0.1"
}

def test_ip_port(ip,port):
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    skt.settimeout(3)
    try:
        ex_code = skt.connect_ex((ip, int(port)))
        # a = s.connect((ip, int(port)))
        # s.shutdown(socket.SHUT_RDWR)
        print(ex_code)
    except Exception as e:
        print(e)
    finally:
        skt.close()

def pull_proxy_site():
    pass

def request_with_proxy(url_body,ip,port,kind):
    cur_url = url_body.format(kind)
    cur_proxy = {kind: http_D[kind]}
    print(http_D[kind])

    try:
        r = requests.get(cur_url, headers=headers, proxies=cur_proxy,timeout=5)
        print(r)
        # print(r.json())
    except Exception as e:
        # print("- Connection failed!")
        print(e)

# request_with_proxy(url,ip,port,kind)
# o = subprocess.call("D:/tcping/tcping.exe -n 1 111.222.141.127 8118".split(), stdout=open(os.devnull,"w"), stderr=subprocess.STDOUT)
# o = subprocess.call("D:/tcping/tcping.exe -n 1 123.163.24.113 3128".split())
# print(o)

