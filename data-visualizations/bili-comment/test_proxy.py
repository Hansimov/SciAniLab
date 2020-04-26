import os
import sys
import time
import datetime
import random
import re
import subprocess
import requests
import socket
import json
import threading
import multiprocessing

# ip, port, kind = "117.88.176.162", "3000", "https"
# ip, port, kind = "124.156.98.172", "80", "http"


kind_D = {
    "http":  "http://{}:{}",
    "https": "https://{}:{}",
    "ftp":   "ftp://{}:{}"
}

headers = {
    "user-agent": "skynet - {}".format(random.random())
}

def dt2str(dt_time):
    return "{:>4}-{:0>2}-{:0>2}-{:0>2}-{:0>2}-{:0>2}".format(dt_time.year, dt_time.month, dt_time.day, dt_time.hour, dt_time.minute, dt_time.second)

def str2dt(dt_str):
    return datetime.datetime.strptime(dt_str,'%Y-%m-%d-%H-%M-%S')

def now():
    return datetime.datetime().now()

def is_any_thread_alive(threads):
    return True in [t.is_alive() for t in threads]

def fetch_xici():
    # tmp_proxy = {"https":"https://117.45.139.84:9006"}
    # tmp_proxy = {"http":"http://52.69.132.45:8080"}
    # req = requests.get("http://www.xicidaili.com/nn/1",headers=headers,proxies=tmp_proxy)
    req = requests.get("http://www.xicidaili.com/nn/1",headers=headers)
    print("=== Fetching xici {} ===\n".format(req.status_code))
    sys.stdout.flush()

    # text = req.text
    with open("example.html","wb") as wf:
        wf.write(req.content)
    with open("example.html",mode="r",encoding="utf-8") as rf:
        text = rf.read()
        
    text = re.findall(r"<table[\s\S]*?table>", text)[0]
    tr_L = re.findall(r"<tr class[\s\S]*?tr>", text)

    ip_L = []
    for tr in tr_L:
        td_L = re.findall(r"<td>([\s\S]*?)</td>",tr)
        ip = [td_L[0],td_L[1],td_L[-1]]
        # for td in td_L:
        #     if "href" in td or "\n" in td:
        #         continue
        #     ip.append(td)
        ip_L.append(ip)
    # ip, port, http(s)
    return ip_L

def fetch_free_proxy():
    old_filename = ""
    for filename in os.listdir():
        if re.match("free-proxy-list-[\s\S]*",filename):
            old_filename = filename
            break

    new_dt_time = datetime.datetime.now()

    is_fetch_new_proxy = False

    if old_filename == "":
        is_fetch_new_proxy = True
    else:
        old_dt_str = old_filename.replace("free-proxy-list-","").replace(".html","")
        old_dt_time = str2dt(old_dt_str)
        if (new_dt_time-old_dt_time).total_seconds() > 300:
            os.remove(old_filename)
            is_fetch_new_proxy = True

    if is_fetch_new_proxy:
        url = "https://free-proxy-list.net/"
        req = requests.get(url,headers=headers)
        print("=== Fetching free-proxy-list {} ===\n".format(req.status_code))
        new_filename = "free-proxy-list-{}.html".format(dt2str(new_dt_time))
        with open(new_filename,"wb") as wf:
            wf.write(req.content)
        read_filename = new_filename
    else:
        print("=== Reusing {}\n".format(old_filename))
        read_filename = old_filename

    with open(read_filename,mode="r",encoding="utf-8") as rf:
        text = rf.read()

    text = re.findall(r"<tbody[\s\S]*?tbody>", text)[0]
    tr_L = re.findall(r"<tr[\s\S]*?tr>", text)

    ip_L = []
    for tr in tr_L:
        td_L = re.findall(r"<td[\s\S]*?>([\s\S]*?)</td>",tr)
        kind = "http" if td_L[-2]== "no" else "https"
        ip = [td_L[0],td_L[1],kind]
        ip_L.append(ip)
    # ip, port, http(s)
    return ip_L


req_retry_max = 3
url_body = "{}://api.bilibili.com/x/v2/reply?pn={}&type=1&oid={}&nohot=1&sort=2"
test_url_body = "{}://api.bilibili.com/x/v2/reply?pn=1&type=1&oid=34354599&nohot=1&sort=2"
def request_with_proxy(url_body,ip,port,kind,retry_max=req_retry_max,timeout=6):
    kind = kind.lower()
    cur_url = url_body.format(kind)
    cur_proxy = {kind: kind_D[kind].format(ip,port)}

    retry_cnt = 0
    while (retry_cnt<req_retry_max):
        try:
            r = requests.get(cur_url, headers=headers, proxies=cur_proxy,timeout=timeout)
            status_code = r.status_code
            # return status_code
            # return retry_cnt
            break
        except Exception as e:
            # print(e)
            retry_cnt += 1
    return retry_cnt

valid_ip_L = []
def test_ip_port(ip, port, kind="http",retry_max=3,timeout=4):
    global valid_ip_cnt, valid_ip_L
    sema.acquire()

    ret = 0
    req_cnt = request_with_proxy(test_url_body,ip,port,kind)

    lock.acquire()
    # sys.stdout.flush()
    if req_cnt <= 1:
        ret = 1
        # ip, port, kind, last_used_time, req_cnt, hit_cnt
        valid_ip_L.append([ip,port,kind,datetime.datetime.now(),0,0])
        valid_ip_cnt += ret
        print("{:<3} {:<15} {:<5} {:<5}".format((3-req_cnt)*"+",ip,port,kind.upper()))
    else:
        print("{:<3} {:<15} {:<5} {:<5}".format(3*"-",ip,port,kind.upper()))

    lock.release()
    sema.release()


valid_ip_cnt = 0
max_concurrent_num = 50
sema = threading.BoundedSemaphore(max_concurrent_num)
lock = threading.Lock()

def sieve_valid_ip_list():
    # ip_L = fetch_xici()
    ip_L = fetch_free_proxy()

    total_ip_cnt = len(ip_L)

    pool = []
    for i in range(total_ip_cnt):
        ip,port,kind = ip_L[i][0:3]
        tmp_thread = threading.Thread(target=test_ip_port, args=(ip,port,kind,), daemon=True)
        pool.append(tmp_thread)
    for tmp_thread in pool:
        tmp_thread.start()

    while is_any_thread_alive(pool):
        time.sleep(0)

    print("\nValid IP: {}/{}".format(valid_ip_cnt, total_ip_cnt))
    for valid_ip in valid_ip_L:
        print("   {:<15} {:<5} {:<5}".format(*valid_ip[:3]))

def put_back_used_ip(ip,req_cnt):
    global valid_ip_L, valid_ip_cnt
    # ip, port, kind, last_used_time, req_cnt, hit_cnt
    if req_cnt < req_retry_max:
        ip[3] = datetime.datetime.now()
        ip[-1] += 1
        ip[-2] += req_cnt
        valid_ip_L.append(ip)
    else:
        valid_ip_cnt -= 1

wait_second = 0.1
valid_ip_cnt
def take_out_valid_ip():
    global valid_ip_L
    for i,ip in enumerate(valid_ip_L):
        if (now()-ip[3]).total_seconds() > wait_second:
            valid_ip_L.pop(i)
            return ip
    return []

def get_ip_address():
    url = "{}://icanhazip.com/"
    pass

def get_replies(oid="34354599"):
    pass
    # url = url_body.format(kind,pn,oid)


if __name__ == '__main__':

    # t1 = time.time()
    sieve_valid_ip_list()
    # t2 = time.time()
    # print("Elapsed time: {} sec".format(round(t2-t1,2)))

    # p1 = Process(target=func1)
    # p1.start()
    # p2 = Process(target=func2)



    # fetch_free_proxy()


