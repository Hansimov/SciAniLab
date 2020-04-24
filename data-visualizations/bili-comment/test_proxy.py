import os
import subprocess
import requests
import json

# ip, port, kind = "117.88.176.162", "3000", "https"
ip, port, kind = "122.224.65.201", "3128", "https"

url = "{}://api.bilibili.com/x/v2/reply?pn=1&type=1&oid=667592495&sort=2&_=1587689751023"

proxy_D = {
    "http":  "http://{}:{}".format(ip,port),
    "https": "https://{}:{}".format(ip,port),
    "ftp":   "ftp://{}:{}".format(ip,port)
}

headers = {
    "user-agent": "my-app/0.0.1"
}

def request_with_proxy(url_body,ip,port,kind):
    cur_url = url_body.format(kind)
    cur_proxy = {kind: proxy_D[kind]}
    print(proxy_D[kind])

    try:
        r = requests.get(cur_url, headers=headers, proxies=cur_proxy,timeout=6)
        print(r)
        # print(r.json())
    except Exception as e:
        # print("- Connection failed!")
        print(e)

# request_with_proxy(url,ip,port,kind)
o = subprocess.call("D:/tcping/tcping.exe -n 1 111.222.141.127 8118".split(), stdout=open(os.devnull,"w"), stderr=subprocess.STDOUT)
# o = os.system()
print(o)