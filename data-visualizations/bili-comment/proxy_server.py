import os
import re
import datetime
import time
import random
import requests
# import base64
import sys
import socket
import threading
import pickle
import eventlet
eventlet.monkey_patch(thread=False)

last_fetch_proxy_time = 0

def headers():
    return { "user-agent": "botnet - {}".format(random.random()) }

def dt2str(dt_time):
    return "{:>4}-{:0>2}-{:0>2}-{:0>2}-{:0>2}-{:0>2}".format(dt_time.year, dt_time.month, dt_time.day, dt_time.hour, dt_time.minute, dt_time.second)

def str2dt(dt_str):
    return datetime.datetime.strptime(dt_str,'%Y-%m-%d-%H-%M-%S')

# ========================= Fetch proxy from sites ========================= #
html_path = "./px-htmls/"
def get_is_fetch_new_proxy(site_name):
    global last_fetch_proxy_time
    site_name = site_name
    old_filename = ""
    for filename in os.listdir(html_path):
        if re.match(site_name+"-[\s\S]*",filename):
            old_filename = html_path+filename
            break

    new_dt_time = datetime.datetime.now()
    new_filename = html_path+"{}-{}.html".format(site_name, dt2str(new_dt_time))
    last_fetch_proxy_time = time.time()

    is_fetch_new_proxy = False
    if old_filename == "":
        is_fetch_new_proxy = True
    else:
        old_dt_str = old_filename.replace(html_path,"").replace(site_name+"-","").replace(".html","")
        old_dt_time = str2dt(old_dt_str)
        if (new_dt_time-old_dt_time).total_seconds() > 300:
            os.remove(old_filename)
            is_fetch_new_proxy = True

    return is_fetch_new_proxy, old_filename, new_filename

def fetch_free_proxy_list_net():
    """ return 2d list of [ip, port, kind, last_used_time] """
    site_name = "free-proxy-list"
    is_fetch_new_proxy, old_filename, new_filename = get_is_fetch_new_proxy(site_name)

    if is_fetch_new_proxy:
        url = "https://free-proxy-list.net/"
        req = requests.get(url,headers=headers())
        print("=== Fetching {} {} ===\n".format(site_name, req.status_code))
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

def fetch_xici_daili():
    """ return 2d list of [ip, port, kind, last_used_time] """
    site_name = "xici-daili"
    suffix_L = ["nn","nt","wn","wt"]
    fetched_proxy_L = []
    for suffix in suffix_L:
        for page in range(1,2):
            is_fetch_new_proxy, old_filename, new_filename = get_is_fetch_new_proxy("{}-{}-{}".format(site_name,suffix,page))

            if is_fetch_new_proxy:
                url = "http://www.xicidaili.com/{}/{}".format(suffix,page)
                req = requests.get(url, headers=headers())
                print("=== Fetching {}-{}-{} {} ===\n".format(site_name, suffix, page, req.status_code))
                with open(new_filename,"wb") as wf:
                    wf.write(req.content)
                read_filename = new_filename
            else:
                print("=== Reusing {}\n".format(old_filename))
                read_filename = old_filename

            with open(read_filename,mode="r",encoding="utf-8") as rf:
                text = rf.read()

            text = re.findall(r"<table[\s\S]*?table>", text)[0]
            tr_L = re.findall(r"<tr class[\s\S]*?tr>", text)

            for tr in tr_L:
                td_L = re.findall(r"<td>([\s\S]*?)</td>",tr)
                proxy = [td_L[0], td_L[1], td_L[3]]
                if "socks" in proxy[2].lower():
                    continue
                fetched_proxy_L.append(proxy)
    # ip, port, http(s)
    return fetched_proxy_L

def fetch_66ip():
    """ return 2d list of [ip, port, kind, last_used_time] """
    # Many duplicates of xici, low usable ratio
    site_name = "66ip"
    is_fetch_new_proxy, old_filename, new_filename = get_is_fetch_new_proxy(site_name)
    if is_fetch_new_proxy:
        url = "http://www.66ip.cn/mo.php?sxb=&tqsl=1000"
        req = requests.get(url,headers=headers())
        print("=== Fetching 66ip {} ===\n".format(req.status_code))
        with open(new_filename,"wb") as wf:
            wf.write(req.content)
        read_filename = new_filename
    else:
        print("=== Reusing {}\n".format(old_filename))
        read_filename = old_filename

    with open(read_filename,mode="r",encoding="windows-1252") as rf:
        text = rf.read()

    text = re.findall(r"(.*)<br\s/>", text)
    fetched_proxy_L = []
    for line in text:
        ip,port = line.strip().split(":")
        kind = "http"
        proxy = [ip,port,kind]
        fetched_proxy_L.append(proxy)
    # ip, port, http(s)
    return fetched_proxy_L

# # deprecated, todo
# def fetch_free_proxy_cz():
#     """ return 2d list of [ip, port, kind, last_used_time] """
#     # Banned by GFW sometimes
#     site_name = "free-proxy-cz"
#     is_fetch_new_proxy, old_filename, new_filename = get_is_fetch_new_proxy(site_name)
#     if is_fetch_new_proxy:
#         url = "http://free-proxy.cz/en/proxylist/country/CN/all/ping/all/2"
#         try:
#             with eventlet.Timeout(6):
#                 req = requests.get(url, headers=headers())
#         except:
#             print("x Fetching free-proxy-cz failed!")
#             return
#         print("=== Fetching {} {} ===\n".format(site_name, req.status_code))
#         with open(new_filename,"wb") as wf:
#             wf.write(req.content)
#         read_filename = new_filename
#     else:
#         print("=== Reusing {}\n".format(old_filename))
#         read_filename = old_filename

#     with open(read_filename,mode="r",encoding="utf-8") as rf:
#         text = rf.read()
#     # print(text)
#     text = re.findall(r"<tbody[\s\S]*?tbody>", text)[0]
#     tr_L = re.findall(r"<tr[\s\S]*?tr>", text)
#     # print(len(tr_L))

#     fetched_proxy_L = []
#     for tr in tr_L:
#         td_L = re.findall(r"<td[\s\S]*?td>", text)
#         ip_b64 = re.findall(r"decode\(\"([\s\S]*?)\"\)", td_L[0])
#         print(ip_b64)
#         ip_b64 = ip_b64.replace("decode","").replace("(","").replace(")","").replace("\"","")
#         ip = base64.b64decode(ip_b64)
#         print(ip)
#         # todo
#         # fetched_proxy_L.append(proxy)

#     # ip, port, http(s)
#     return fetched_proxy_L

def fetch_jiangxianli():
    """ return 2d list of [ip, port, kind, last_used_time] """
    site_name = "jiangxianli"
    fetched_proxy_L = []
    for page in range(1,16):
        is_fetch_new_proxy, old_filename, new_filename = get_is_fetch_new_proxy("{}-{}".format(site_name,page))

        if is_fetch_new_proxy:
            # Fetching the site directly will fail when the site is refreshing
            # url = "https://ip.jiangxianli.com/?page={}".format(page)
            url = "https://ip.jiangxianli.com/api/proxy_ips?page={}".format(page)
            
            status_code = -1
            while status_code != 200:
                try:
                    req = requests.get(url, headers=headers())
                    status_code = req.status_code
                except:
                    continue

            print("=== Fetching {}-{} {} ===\n".format(site_name, page, status_code))
            with open(new_filename,"wb") as wf:
                wf.write(req.content)
            read_filename = new_filename
            # if page % 3 == 1:
            #     time.sleep(0.5)
        else:
            print("=== Reusing {}\n".format(old_filename))
            read_filename = old_filename

        # print(read_filename)
        with open(read_filename,mode="r",encoding="utf-8") as rf:
            text = rf.read()

        # return

        # text = re.findall(r"<tbody[\s\S]*?tbody>", text)[0]
        # tr_L = re.findall(r"<tr[\s\S]*?tr>", text)
        # for tr in tr_L:
        #     td_L = re.findall(r"<td>([\s\S]*?)</td>",tr)
        #     proxy = [td_L[0], td_L[1], td_L[3]]
        #     # print(*proxy)
        #     fetched_proxy_L.append(proxy)

        item_L = re.findall(r'"ip".*?port.*?,', text)
        for item in item_L:
            ip = re.findall(r'"ip":"(.*?)"', item)[0]
            port = re.findall(r'"port":"(.*?)"', item)[0]
            kind = "http"
            fetched_proxy_L.append([ip,port,kind])

    # ip, port, http(s)
    return fetched_proxy_L

def fetch_xila_daili():
    """ return 2d list of [ip, port, kind, last_used_time] """
    site_name = "xila-daili"
    # suffix_L = ["putong", "gaoni"]
    suffix_L = ["putong", "gaoni", "https","http"]
    page_L = [1,1,1,1]
    fetched_proxy_L = []
    for i,suffix in enumerate(suffix_L):
        for page in range(1, page_L[i]+1):
            is_fetch_new_proxy, old_filename, new_filename = get_is_fetch_new_proxy("{}-{}-{}".format(site_name,suffix,page))
            if is_fetch_new_proxy:
                url = "http://www.xiladaili.com/{}/{}/".format(suffix,page)
                status_code = -1
                while status_code != 200:
                    try:
                        req = requests.get(url, headers=headers())
                        status_code = req.status_code
                    except:
                        time.sleep(0.5)
                        continue

                print("=== Fetching {}-{}-{} {} ===\n".format(site_name, suffix, page, req.status_code))
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

            for tr in tr_L:
                td_L = re.findall(r"<td>([\s\S]*?)</td>",tr)
                ip,port = td_L[0].split(":")
                kind = "http" if "http" in td_L[1].lower() else "https"
                proxy = [ip,port,kind]

                # print(*proxy)
                fetched_proxy_L.append(proxy)
    # ip, port, http(s)
    return fetched_proxy_L

def fetch_foxtools():
    """ return 2d list of [ip, port, kind, last_used_time] """
    site_name = "foxtools"
    fetched_proxy_L = []
    for page in range(1,3):
        is_fetch_new_proxy, old_filename, new_filename = get_is_fetch_new_proxy("{}-{}".format(site_name,page))

        if is_fetch_new_proxy:
            url = "http://api.foxtools.ru/v2/Proxy.txt?page={}".format(page)
            req = requests.get(url, headers=headers())
            status_code = req.status_code

            print("=== Fetching {}-{} {} ===\n".format(site_name, page, status_code))
            with open(new_filename,"wb") as wf:
                wf.write(req.content)
            read_filename = new_filename
        else:
            print("=== Reusing {}\n".format(old_filename))
            read_filename = old_filename

        with open(read_filename,mode="r",encoding="utf-8") as rf:
            text = rf.readlines()
        
        for line in text[1:]:
            ip,port = line.strip().split(":")
            kind = "http"
            proxy = [ip,port,kind]
            fetched_proxy_L.append(proxy)

    # ip, port, http(s)
    return fetched_proxy_L
def fetch_proxy_list_download():
    """ return 2d list of [ip, port, kind, last_used_time] """
    site_name = "proxy-list-download"
    fetched_proxy_L = []
    # suffix_L = ["http", "https"]
    suffix_L = ["http"]
    for suffix in suffix_L:
        is_fetch_new_proxy, old_filename, new_filename = get_is_fetch_new_proxy("{}-{}".format(site_name,suffix))

        if is_fetch_new_proxy:
            url = "https://www.proxy-list.download/api/v1/get?type={}".format(suffix)
            req = requests.get(url, headers=headers())
            status_code = req.status_code

            print("=== Fetching {}-{} {} ===\n".format(site_name, suffix, status_code))
            with open(new_filename,"wb") as wf:
                wf.write(req.content)
            read_filename = new_filename
        else:
            print("=== Reusing {}\n".format(old_filename))
            read_filename = old_filename

        with open(read_filename,mode="r",encoding="utf-8") as rf:
            text = rf.readlines()
        
        for line in text:
            ip,port = line.strip().split(":")
            kind = suffix
            proxy = [ip,port,kind]
            fetched_proxy_L.append(proxy)

    # ip, port, http(s)
    return fetched_proxy_L

def fetch_nima_daili():
    """ return 2d list of [ip, port, kind, last_used_time] """
    site_name = "nima-daili"
    # suffix_L = ["putong", "gaoni"]
    suffix_L = ["https","http"]
    page_L = [2,2]
    fetched_proxy_L = []
    for i,suffix in enumerate(suffix_L):
        for page in range(1, page_L[i]+1):
            is_fetch_new_proxy, old_filename, new_filename = get_is_fetch_new_proxy("{}-{}-{}".format(site_name,suffix,page))
            if is_fetch_new_proxy:
                url = "http://www.nimadaili.com/{}/{}/".format(suffix,page)
                # status_code = -1
                # while status_code != 200:
                #     try:
                req = requests.get(url, headers=headers())
                # status_code = req.status_code
                    # except:
                    #     time.sleep(0.5)
                    #     continue

                print("=== Fetching {}-{}-{} {} ===\n".format(site_name, suffix, page, req.status_code))
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

            for tr in tr_L:
                td_L = re.findall(r"<td>([\s\S]*?)</td>",tr)
                ip,port = td_L[0].split(":")
                kind = "http" if "http" in td_L[1].lower() else "https"
                proxy = [ip,port,kind]

                fetched_proxy_L.append(proxy)
    # ip, port, http(s)
    return fetched_proxy_L

# https://proxylist.me/?page=1

# http://spys.one/free-proxy-list/

# xxxxxxxxxxxxxxxxxxxxxx End of Fetch proxy from sites xxxxxxxxxxxxxxxxxxxxxx #


valid_proxy_L, invalid_proxy_L = [], []

def is_any_thread_alive(threads):
    return True in [t.is_alive() for t in threads]

def is_proxy_in_proxy_L(proxy, proxy_L, valid_proxy_L_lock):
    valid_proxy_L_lock.acquire()

    proxy[2] = proxy[2].lower()
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


req_retry_max = 3
req_timeout = 3.0
# reply_url_body = "{}://api.bilibili.com/x/v2/reply?pn={}&type=1&oid={}&nohot=1&sort=2"
def request_with_proxy(test_url_body,ip,port,kind,retry_max=req_retry_max,timeout=req_timeout):
    kind = kind.lower()
    cur_url = test_url_body.format(kind)
    cur_proxy = ip_port_to_proxy(ip,port,kind)

    status_code = -1
    retry_cnt = 0
    while (retry_cnt<req_retry_max):
        try:
            with eventlet.Timeout(timeout):
                r = requests.get(cur_url, headers=headers(), proxies=cur_proxy)
                status_code = r.status_code
                # sys.stdout.flush()
            break
        except:
            # print(e)
            retry_cnt += 1
    return retry_cnt, status_code

def check_proxy_validity(proxy, check_proxy_validity_sema, valid_proxy_L_lock):
    global valid_proxy_L, invalid_proxy_L

    check_proxy_validity_sema.acquire()
    ip, port, kind = proxy[:3]
    kind = kind.lower()

    req_cnt = req_retry_max
    is_proxy_valid = False

    if is_proxy_in_proxy_L(proxy, valid_proxy_L, valid_proxy_L_lock):
        is_proxy_valid = True
        # print("{:<15} {:<5} {:<5} in valid_proxy_L!".format(*proxy[:3]))
        check_proxy_validity_sema.release()
        return

    if is_proxy_in_proxy_L(proxy, invalid_proxy_L, valid_proxy_L_lock):
        # print("{:<15} {:<5} {:<5} in invalid_proxy_L!".format(*proxy[:3]))
        check_proxy_validity_sema.release()
        return

    test_url_body = "{}://api.bilibili.com/x/v2/reply?pn=1&type=1&oid=34354599&nohot=1&sort=2"
    t1 = time.time()
    req_cnt, status_code = request_with_proxy(test_url_body,ip,port,kind)
    t2 = time.time()

    # sys.stdout.flush()
    if status_code==200 and req_cnt <= 1:
        # ip, port, kind, last_used_time, delay
        is_proxy_valid = True

    if is_proxy_valid:
        delta_t = round(t2-t1,1)
        tmp_proxy = [ip, port, kind, time.time(), delta_t]
        if not is_proxy_in_proxy_L(tmp_proxy, valid_proxy_L, valid_proxy_L_lock):
            valid_proxy_L_lock.acquire()
            valid_proxy_L.append(tmp_proxy)
            valid_proxy_L_lock.release()
    #     else:
    #         print("same valid proxy!")
    # else:
    #     delta_t = req_retry_max*req_timeout
    #     tmp_proxy = [ip, port, kind, time.time(), delta_t]
    #     if not is_proxy_in_proxy_L(tmp_proxy, invalid_proxy_L, valid_proxy_L_lock):
    #         valid_proxy_L_lock.acquire()
    #         invalid_proxy_L.append(tmp_proxy)
    #         valid_proxy_L_lock.release()
    #     else:
    #         print("same invalid proxy!")

    if is_proxy_valid:
        print("{:<3} {:<15} {:<5} {:<5} {:<3} {:>4}s".format((3-req_cnt)*"+", ip, port, kind, status_code, delta_t))

    check_proxy_validity_sema.release()

update_valid_proxy_interval = 200
def update_valid_proxy():
    """ update valid_proxy_L and invalid_proxy_L: 
        2d list of [ip, port, kind, last_used_time, delay]
    """
    global valid_proxy_L

    # print(time.time(), last_fetch_proxy_time)
    if time.time() - last_fetch_proxy_time < update_valid_proxy_interval:
        return

    fetched_proxy_L = []
    fetched_proxy_L.extend(fetch_free_proxy_list_net())
    fetched_proxy_L.extend(fetch_jiangxianli())
    fetched_proxy_L.extend(fetch_proxy_list_download())
    # fetched_proxy_L.extend(fetch_xici_daili())
    # fetched_proxy_L.extend(fetch_foxtools())
    # fetched_proxy_L.extend(fetch_xila_daili())
    # fetched_proxy_L.extend(fetch_nima_daili())
    # fetched_proxy_L.extend(fetch_66ip())
    # fetched_proxy_L.extend(fetch_free_proxy_cz())
    # return
    check_proxy_validity_sema = threading.BoundedSemaphore(len(fetched_proxy_L))
    # check_proxy_validity_sema = threading.BoundedSemaphore(500)

    valid_proxy_L = []
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

    print("valid proxy count: {}/{}".format(len(valid_proxy_L), len(fetched_proxy_L)))
    # print("valid proxy count: {}/{}/{}".format(len(valid_proxy_L), len(valid_proxy_L)+len(invalid_proxy_L), len(fetched_proxy_L)))

# reuse_interval = 1.0
# def select_valid_proxy(conn, data):
#     global valid_proxy_L, invalid_proxy_L
#     if data[0] == "get":
#         if len(valid_proxy_L) > 0:
#             proxy = valid_proxy_L[0]
#             if time.time() - proxy[3] > reuse_interval:
#                 proxy_pkl = pickle.dumps(proxy)
#                 conn.sendall(proxy_pkl)
#                 print("> Send {:<15} {:<5} {:<5}".format(*proxy[:3]))
#                 proxy[3] = time.time()
#                 valid_proxy_L.append(proxy)
#                 valid_proxy_L.pop(0)
#         conn.sendall(pickle.dumps([]))
#     elif data[0] == "del":
#         for i in range(len(valid_proxy_L)):
#             proxy = valid_proxy_L[i]
#             if data[1][:3] == proxy[:3]:
#                 invalid_proxy_L.append(valid_proxy_L.pop(i))
#                 print("x Invalid {:<15} {:<5} {:<5}".format(*proxy[:3]))
#                 break
#     else:
#         pass

def send_valid_proxy_L(conn,data):
    if data[0] == "get":
        print("> Send valid_proxy_L num: {}".format(len(valid_proxy_L)))
        conn.sendall(pickle.dumps(valid_proxy_L))
    else:
        # print("> Send empty list")
        # conn.sendall(pickle.dumps([]))
        pass

# fetch proxies in advance
# if a proxy in client is invalid, then the client requests for a new proxy
# server returns a valid proxy when receiving a client request
socket_timeout = 1
def run_proxy_server(timeout=socket_timeout):
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
                    # select_valid_proxy(conn,data)
                    send_valid_proxy_L(conn,data)
            except socket.timeout:
                # print("Waiting for command ...")
                update_valid_proxy()
            except KeyboardInterrupt:
                break
    except KeyboardInterrupt:
        print("Server closed with KeyboardInterrupt!")

if __name__ == '__main__':
    run_proxy_server()