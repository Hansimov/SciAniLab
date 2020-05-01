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
# import gevent
import eventlet
eventlet.monkey_patch(thread=False)


kind_D = {
    "http":  "http://{}:{}",
    "https": "https://{}:{}",
    "ftp":   "ftp://{}:{}"
}

def headers():
    return { "user-agent": "botnet - {}".format(random.random()) }

def dt2str(dt_time):
    return "{:>4}-{:0>2}-{:0>2}-{:0>2}-{:0>2}-{:0>2}".format(dt_time.year, dt_time.month, dt_time.day, dt_time.hour, dt_time.minute, dt_time.second)

def str2dt(dt_str):
    return datetime.datetime.strptime(dt_str,'%Y-%m-%d-%H-%M-%S')

# def now():
#     return datetime.datetime().now()

def is_any_thread_alive(threads):
    return True in [t.is_alive() for t in threads]


def fetch_free_proxy_from_web():
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
        req = requests.get(url,headers=headers())
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

    proxy_L = []
    for tr in tr_L:
        td_L = re.findall(r"<td[\s\S]*?>([\s\S]*?)</td>",tr)
        kind = "http" if td_L[-2]== "no" else "https"
        proxy = [td_L[0],td_L[1],kind]
        proxy_L.append(proxy)
    # ip, port, http(s)
    return proxy_L


req_retry_max = 3
url_body = "{}://api.bilibili.com/x/v2/reply?pn={}&type=1&oid={}&nohot=1&sort=2"
test_url_body = "{}://api.bilibili.com/x/v2/reply?pn=1&type=1&oid=34354599&nohot=1&sort=2"
def request_with_proxy(url_body,ip,port,kind,retry_max=req_retry_max,timeout=3):
    kind = kind.lower()
    cur_url = url_body.format(kind)
    cur_proxy = {kind: kind_D[kind].format(ip,port)}

    retry_cnt = 0
    # t1 = time.time()
    while (retry_cnt<req_retry_max):
        try:
            with eventlet.Timeout(timeout):
                r = requests.get(cur_url, headers=headers(), proxies=cur_proxy)
                status_code = r.status_code
            break
        except:
            # print(e)
            retry_cnt += 1
    return retry_cnt

valid_proxy_L = []
def check_proxy_validity(proxy, check_proxy_connection_sema, valid_proxy_L_lock):
    global valid_proxy_L

    check_proxy_connection_sema.acquire()

    ip, port, kind = proxy[:3]
    ret = 0

    t1 = time.time()
    req_cnt = request_with_proxy(test_url_body,ip,port,kind)
    t2 = time.time()

    delta_t = round(t2-t1,1)

    # sys.stdout.flush()
    if req_cnt <= 1:
        ret = 1
        # ip, port, kind, last_used_time, last_delay, req_cnt, hit_cnt
        valid_proxy_L_lock.acquire()
        valid_proxy_L.append([ip, port, kind, time.time(), delta_t, req_cnt+1, 1])
        valid_proxy_L[0] += 1
        valid_proxy_L_lock.release()
        # valid_ip_cnt += ret
    
    print("{:<3} {:<15} {:<5} {:<5} {:>4}s".format((3-req_cnt)*"+", ip, port, kind.upper(),delta_t))

    check_proxy_validity_sema.release()

def fetch_proxy

def check_proxy_validity_multi():
    global valid_proxy_L
    proxy_L = fetch_free_proxy_from_web()

    check_proxy_validity_sema = threading.BoundedSemaphore(len(proxy_L))

    valid_proxy_L_lock = threading.Lock()

    valid_proxy_L.append(0)
    pool = []
    for i in range(len(proxy_L)):
        # ip,port,kind = proxy_L[i][0:3]
        proxy = proxy_L[i][:3]
        tmp_thread = threading.Thread(target=check_proxy_validity, args=(proxy,  check_proxy_validity_sema, valid_proxy_L_lock), daemon=True)
        pool.append(tmp_thread)

    for tmp_thread in pool:
        tmp_thread.start()
    for tmp_thread in pool:
        tmp_thread.join()

    # while is_any_thread_alive(pool):
    #     time.sleep(0)

    # print("\nValid IP: {}/{}".format(valid_ip_cnt, total_ip_cnt))
    # for valid_ip in valid_proxy_L:
    #     print("   {:<15} {:<5} {:<5}".format(*valid_ip[:3]))


def disp_proxy(disp_proxy_sema, valid_proxy_L_lock):
    disp_proxy_sema.acquire()
    # url = "{}://icanhazip.com/"
    time.sleep(0.5 + random.random())

    disp_proxy_sema.release()

def disp_proxy_multi(valid_proxy_L):
    disp_proxy_sema = threading.BoundedSemaphore(5)
    valid_proxy_L_lock = threading.Lock()

    # time.sleep(5)
    pool = []
    for i in range(100):
        tmp_thread = threading.Thread(target=disp_proxy, args=(disp_proxy_sema, valid_proxy_L_lock), daemon=True)
        pool.append(tmp_thread)

    for tmp_thread in pool:
        tmp_thread.start()
    for tmp_thread in pool:
        tmp_thread.join()
    # while is_any_thread_alive(pool):
    #     time.sleep(0)


def get_replies(oid="34354599"):
    pass
    # url = url_body.format(kind,pn,oid)

if __name__ == '__main__':
    t1 = time.time()
    check_proxy_validity_multi()
    # run_threads_disp_proxy()

    t2 = time.time()
    print("valid_proxy_L count: {}".format(valid_proxy_L[0]))
    print("Total time: {} sec".format(round(t2-t1,2)))

