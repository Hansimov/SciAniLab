import os
import subprocess
import requests
import socket
import json
import random
import re
import sys
import multiprocessing

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

def test_ip_port(ip,port,retry=3,timeout=3):
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    skt.settimeout(timeout)
    ex_code = skt.connect_ex((ip, int(port)))
    # a = s.connect((ip, int(port)))
    # s.shutdown(socket.SHUT_RDWR)
    # print(ex_code)
    skt.close()

    ret = 0
    if ex_code == 0:
        # print("+++ {}:{} open +++".format(ip,port))
        print("+++ OPEN +++".format(ip,port))
        ret = 1
    else:
        # print("--- {}:{} fail ---".format(ip,port))
        print("------------".format(ip,port))
    sys.stdout.flush()
    return ret


def fetch_proxy_site():
    req = requests.get("https://www.xicidaili.com/nn/",headers=headers)
    print("=== Fetching xici successfully ===")
    sys.stdout.flush()

    # text = req.text
    with open("example.html","wb") as wf:
        wf.write(req.content)
    with open("example.html",mode="r",encoding="utf-8") as rf:
        text = rf.read()
        
    text = re.findall(r"<table[\s\S]*?table>", text)[0]
    res_L = re.findall(r"<tr class[\s\S]*?tr>", text)

    ip_L = []
    for res in res_L:
        item = re.findall(r"<td>([\s\S]*?)</td>",res)
        ip = []
        for it in item:
            if "href" in it or "\n" in it:
                continue
            ip.append(it)
        ip_L.append(ip)
    # ip, port, http(s), alive_time, last_scan_time
    return ip_L


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

ip_L = fetch_proxy_site()

# open_cnt = 0
# total_cnt = len(ip_L)
# # total_cnt = 4
# for ip in ip_L[:total_cnt]:
#     print("{:<15} {:<5} {:<5} {:>6} {:<14}".format(ip[0],ip[1],ip[2],ip[3],ip[4]))
#     open_cnt += test_ip_port(ip[0],ip[1])
# print("Good IP: {}/{}".format(open_cnt,total_cnt))
