import os
import sys
import time
import datetime
import random
import re
import requests
import socket
import threading
import pickle
import eventlet
eventlet.monkey_patch(thread=False)

# fetch proxies in advance
# if a proxy in client is invalid, then the client requests for a new proxy
# server returns a valid proxy when receiving a client request

last_fetch_proxy_time = 0.0

valid_proxy_L, invalid_proxy_L = [], []

def headers():
    return { "user-agent": "botnet - {}".format(random.random()) }

def dt2str(dt_time):
    return "{:>4}-{:0>2}-{:0>2}-{:0>2}-{:0>2}-{:0>2}".format(dt_time.year, dt_time.month, dt_time.day, dt_time.hour, dt_time.minute, dt_time.second)

def str2dt(dt_str):
    return datetime.datetime.strptime(dt_str,'%Y-%m-%d-%H-%M-%S')

def is_any_thread_alive(threads):
    return True in [t.is_alive() for t in threads]

def is_proxy_in_proxy_L(proxy, proxy_L, valid_proxy_L_lock):
    valid_proxy_L_lock.acquire()

    for proxy_tmp in proxy_L:
        if proxy[:3] == proxy_tmp[:3]:
            # print(proxy,proxy_tmp)
            valid_proxy_L_lock.release()
            return True

    valid_proxy_L_lock.release()
    return False

def ip_port_to_proxy(ip,port,kind):
    kind = kind.lower()
    kind_D = {
        "http":  "http://{}:{}",
        "https": "https://{}:{}",
        "ftp":   "ftp://{}:{}"
    }
    return {kind: kind_D[kind].format(ip,port)}

def fetch_free_proxy():
    """ return fetched_proxy_L 
        2d list of [ip, port, kind, last_used_time]
    """
    global last_fetch_proxy_time
    old_filename = ""
    for filename in os.listdir():
        if re.match("free-proxy-list-[\s\S]*",filename):
            old_filename = filename
            break

    new_dt_time = datetime.datetime.now()
    last_fetch_proxy_time = time.time()

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

    fetched_proxy_L = []
    for tr in tr_L:
        td_L = re.findall(r"<td[\s\S]*?>([\s\S]*?)</td>",tr)
        kind = "http" if td_L[-2]== "no" else "https"
        proxy = [td_L[0], td_L[1], kind]
        fetched_proxy_L.append(proxy)
    # ip, port, http(s)
    return fetched_proxy_L


req_retry_max = 3
req_timeout = 3.0
# reply_url_body = "{}://api.bilibili.com/x/v2/reply?pn={}&type=1&oid={}&nohot=1&sort=2"
def request_with_proxy(url_body,ip,port,kind,retry_max=req_retry_max,timeout=req_timeout):
    kind = kind.lower()
    cur_url = url_body.format(kind)
    cur_proxy = ip_port_to_proxy(ip,port,kind)

    retry_cnt = 0
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

def check_proxy_validity(proxy, check_proxy_validity_sema, valid_proxy_L_lock):
    global valid_proxy_L, invalid_proxy_L

    check_proxy_validity_sema.acquire()
    ip, port, kind = proxy[:3]

    req_cnt = req_retry_max
    is_proxy_valid = False
    if is_proxy_in_proxy_L(proxy, invalid_proxy_L, valid_proxy_L_lock):
        pass
    else:
        test_url_body = "{}://api.bilibili.com/x/v2/reply?pn=1&type=1&oid=34354599&nohot=1&sort=2"
        t1 = time.time()
        req_cnt = request_with_proxy(test_url_body,ip,port,kind)
        t2 = time.time()

    # sys.stdout.flush()
    if req_cnt <= 1:
        # ip, port, kind, last_used_time, delay
        is_proxy_valid = True



    if is_proxy_valid:
        delta_t = round(t2-t1,1)
        tmp_proxy = [ip, port, kind, time.time(), delta_t]
        if not is_proxy_in_proxy_L(tmp_proxy, valid_proxy_L, valid_proxy_L_lock):
            valid_proxy_L_lock.acquire()
            valid_proxy_L.append(tmp_proxy)
            valid_proxy_L_lock.release()
    else:
        delta_t = req_retry_max*req_timeout
        tmp_proxy = [ip, port, kind, time.time(), delta_t]
        if not is_proxy_in_proxy_L(tmp_proxy, invalid_proxy_L, valid_proxy_L_lock):
            valid_proxy_L_lock.acquire()
            invalid_proxy_L.append(tmp_proxy)
            valid_proxy_L_lock.release()


    if is_proxy_valid:
        print("{:<3} {:<15} {:<5} {:<5} {:>4}s".format((3-req_cnt)*"+", ip, port, kind, delta_t))

    check_proxy_validity_sema.release()

update_valid_proxy_interval = 30
def update_valid_proxy():
    """ update valid_proxy_L and invalid_proxy_L: 
        2d list of [ip, port, kind, last_used_time, delay]
    """
    if time.time() - last_fetch_proxy_time < update_valid_proxy_interval:
        return
    # fetched_proxy_L = fetch_xici()
    fetched_proxy_L = fetch_free_proxy()
    check_proxy_validity_sema = threading.BoundedSemaphore(len(fetched_proxy_L))

    valid_proxy_L_lock = threading.Lock()

    pool = []
    for i in range(len(fetched_proxy_L)):
        # proxy = fetched_proxy_L[i][:3]
        # ip,port,kind
        proxy = fetched_proxy_L[i]
        tmp_thread = threading.Thread(target=check_proxy_validity, args=(proxy,  check_proxy_validity_sema, valid_proxy_L_lock), daemon=True)
        pool.append(tmp_thread)

    for tmp_thread in pool:
        tmp_thread.start()
    # for tmp_thread in pool:
    #     tmp_thread.join()

    while is_any_thread_alive(pool):
        time.sleep(0)

    print("valid proxy count: {}/{}".format(len(valid_proxy_L), len(valid_proxy_L)+len(invalid_proxy_L)))

reuse_interval = 1.0
def select_valid_proxy(conn, data):
    global valid_proxy_L, invalid_proxy_L
    if data[0] == "get":
        if len(valid_proxy_L) > 0:
            proxy = valid_proxy_L[0]
            if time.time() - proxy[3] > reuse_interval:
                proxy_pkl = pickle.dumps(proxy)
                conn.sendall(proxy_pkl)
                print("> Send {:<15} {:<5} {:<5}".format(*proxy[:3]))
                proxy[3] = time.time()
                valid_proxy_L.append(proxy)
                valid_proxy_L.pop(0)
        conn.sendall(pickle.dumps([]))
    elif data[0] == "del":
        for i in range(len(valid_proxy_L)):
            proxy = valid_proxy_L[i]
            if data[1][:3] == proxy[:3]:
                invalid_proxy_L.append(valid_proxy_L.pop(i))
                print("x Invalid {:<15} {:<5} {:<5}".format(*proxy[:3]))
                break
    else:
        pass


socket_timeout = 1
def run_server(timeout=socket_timeout):
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
                data = pickle.loads(conn.recv(1024))
                if not data:
                    print("x Client disconnected!")
                    break
                else:
                    # print("> Message from client: {}".format(data.decode()))
                    # msg = "> Message from server".format(data.decode()).encode()
                    # conn.sendall(msg)
                    select_valid_proxy(conn,data)
            except socket.timeout:
                # print("Waiting for command ...")
                update_valid_proxy()
            except KeyboardInterrupt:
                break
    except KeyboardInterrupt:
        print("Server closed with KeyboardInterrupt!")

if __name__ == '__main__':
    run_server()

