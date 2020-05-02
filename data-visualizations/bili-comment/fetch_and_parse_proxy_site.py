import os
import re
import datetime
import time
import random
import requests

last_fetch_proxy_time = {}

def headers():
    return { "user-agent": "botnet - {}".format(random.random()) }

def dt2str(dt_time):
    return "{:>4}-{:0>2}-{:0>2}-{:0>2}-{:0>2}-{:0>2}".format(dt_time.year, dt_time.month, dt_time.day, dt_time.hour, dt_time.minute, dt_time.second)

def str2dt(dt_str):
    return datetime.datetime.strptime(dt_str,'%Y-%m-%d-%H-%M-%S')


def get_is_fetch_new_proxy(site_name):
    global last_fetch_proxy_time
    old_filename = ""
    for filename in os.listdir():
        if re.match(site_name+"-[\s\S]*",filename):
            old_filename = filename
            break

    new_dt_time = datetime.datetime.now()

    last_fetch_proxy_time[site_name] = time.time()

    is_fetch_new_proxy = False
    if old_filename == "":
        is_fetch_new_proxy = True
    else:
        old_dt_str = old_filename.replace(site_name+"-","").replace(".html","")
        old_dt_time = str2dt(old_dt_str)
        if (new_dt_time-old_dt_time).total_seconds() > 300:
            os.remove(old_filename)
            is_fetch_new_proxy = True

    return is_fetch_new_proxy, old_filename, new_dt_time

def fetch_free_proxy_list_net():
    """ return fetched_proxy_L 
        2d list of [ip, port, kind, last_used_time]
    """
    is_fetch_new_proxy, old_filename, new_dt_time = get_is_fetch_new_proxy("free-proxy-list")

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