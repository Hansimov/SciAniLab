import os
import subprocess
import requests
import socket
import json
import random
import re

# ip, port, kind = "117.88.176.162", "3000", "https"
ip, port, kind = "124.156.98.172", "80", "http"

url = "{}://api.bilibili.com/x/v2/reply?pn=1&type=1&oid=667592495&sort=2&_=1587689751023"

http_D = {
    "http":  "http://{}:{}".format(ip,port),
    "https": "https://{}:{}".format(ip,port),
    "ftp":   "ftp://{}:{}".format(ip,port)
}

headers = {
    "user-agent": "skynet - {}".format(random.random())
}

def test_ip_port(ip,port,retry=3,timeout=5):
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    skt.settimeout(timeout)
    ex_code = skt.connect_ex((ip, int(port)))
    # a = s.connect((ip, int(port)))
    # s.shutdown(socket.SHUT_RDWR)
    # print(ex_code)
    if ex_code == 0:
        print("+ {}:{} open!".format(ip,port))
    else:
        print("x {}:{} close!".format(ip,port))

    skt.close()

def pull_proxy_site():
    req = requests.get("https://www.xicidaili.com/nn/",headers=headers)
    # print(req)
    # print(req.text[:100])
    with open("example.html",mode="r",encoding="utf-8") as rf:
        text = rf.read()
    text = re.findall(r"<table[\s\S]*?table>", text)[0]
    res_L = re.findall(r"<tr class[\s\S]*?tr>", text)

    for res in res_L:
        item = re.findall(r"<td>([\s\S]*?)</td>",res)
        tmp = []
        for it in item:
            if "href" in it or "\n" in it:
                continue
            tmp.append(it)
        print(tmp)


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

# test_ip_port(ip,port)

pull_proxy_site()