import requests
import datetime
# site_name = "free-proxy-list"

def get_is_fetch_new_proxy(site_name):
    old_filename = ""
    for filename in os.listdir():
        if re.match(site_name+"-[\s\S]*",filename):
            old_filename = filename
            break

    new_dt_time = datetime.datetime.now()
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
    is_fetch_new_proxy, old_filename, new_dt_time = get_is_fetch_new_proxy("free-proxy-list")
    # fetch specific site
    if is_fetch_new_proxy:
        url = "https://free-proxy-list.net/"
        req = requests.get(url,headers=headers())
        print("=== Fetching free-proxy-list {} ===\n".format(req.status_code))
        new_filename = "{}-{}.html".format(site_name,dt2str(new_dt_time))
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


def fetch_xici():
    """ return fetched_proxy_L 
        2d list of [ip, port, kind, last_used_time]
    """
    req = requests.get("http://www.xicidaili.com/nn/1",headers=headers())
    print("=== Fetching xici {} ===\n".format(req.status_code))
    sys.stdout.flush()

    # text = req.text
    with open("example.html","wb") as wf:
        wf.write(req.content)
    with open("example.html",mode="r",encoding="utf-8") as rf:
        text = rf.read()
        
    text = re.findall(r"<table[\s\S]*?table>", text)[0]
    tr_L = re.findall(r"<tr class[\s\S]*?tr>", text)

    proxy_L = []
    for tr in tr_L:
        td_L = re.findall(r"<td>([\s\S]*?)</td>",tr)
        ip = [td_L[0],td_L[1],td_L[-1]]
        # for td in td_L:
        #     if "href" in td or "\n" in td:
        #         continue
        #     ip.append(td)
        proxy_L.append(ip)
    # ip, port, http(s)
    return proxy_L