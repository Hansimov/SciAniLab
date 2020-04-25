import os
import sys
import time
import subprocess
import requests
import socket
import json
import random
import re
import threading

# ip, port, kind = "117.88.176.162", "3000", "https"
# ip, port, kind = "124.156.98.172", "80", "http"

url = "{}://api.bilibili.com/x/v2/reply?pn=1&type=1&oid=667592495&sort=2&_=1587689751023"

http_D = {
    "http":  "http://{}:{}",
    "https": "https://{}:{}",
    "ftp":   "ftp://{}:{}"
}

headers = {
    "user-agent": "skynet - {}".format(random.random())
}


def is_any_thread_alive(threads):
    return True in [t.is_alive() for t in threads]


def fetch_proxy_site():
    req = requests.get("https://www.xicidaili.com/nn/",headers=headers)
    print("=== Fetching xici successfully ===\n")
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


def test_ip_port(ip,port,retry=3,timeout=3):
    global valid_ip_cnt
    sema.acquire()
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    skt.settimeout(timeout)
    ex_code = skt.connect_ex((ip, int(port)))
    # a = s.connect((ip, int(port)))
    # s.shutdown(socket.SHUT_RDWR)
    # print(ex_code)
    skt.close()

    ret = 0
    if ex_code == 0:
        # print("+++ Valid {:>3}.{:>3}.{:>3}.{:>3} : {:<5} +++++++".format(*ip.split("."),port))
        print("+++ Valid {:<15} {:<5} +++++++".format(ip,port))
        ret = 1
    else:
        # print("--------- {:>3}.{:>3}.{:>3}.{:>3} : {:<5} -------".format(*ip.split("."),port))
        print("--------- {:<15} {:<5} -------".format(ip,port))
    lock.acquire()
    sys.stdout.flush()
    valid_ip_cnt += ret
    lock.release()
    sema.release()

def request_with_proxy(url_body,ip,port,kind):
    cur_url = url_body.format(kind)
    cur_proxy = {kind: http_D[kind].format(ip,port)}
    print(http_D[kind])

    try:
        r = requests.get(cur_url, headers=headers, proxies=cur_proxy,timeout=5)
        print(r)
        # print(r.json())
    except Exception as e:
        # print("- Connection failed!")
        print(e)


if __name__ == '__main__':
    ip_L = fetch_proxy_site()
    # request_with_proxy(url,ip,port,kind)
    # test_ip_port(ip,port)
    max_concurrent_num = 40
    sema = threading.BoundedSemaphore(max_concurrent_num)
    lock = threading.Lock()

    total_ip_cnt = len(ip_L)
    valid_ip_cnt = 0

    pool = []
    for i in range(total_ip_cnt):
        ip,port = ip_L[i][0:2]
        tmp_thread = threading.Thread(target=test_ip_port, args=(ip,port,), daemon=True)
        pool.append(tmp_thread)
    for tmp_thread in pool:
        tmp_thread.start()

    while is_any_thread_alive(pool):
        time.sleep(0)

    print("Valid IP: {}/{}".format(valid_ip_cnt, total_ip_cnt))
