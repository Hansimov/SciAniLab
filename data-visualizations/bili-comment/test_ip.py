import requests
import random

headers = {
    "user-agent": "skynet - {}".format(random.random())
}

kind_D = {
    "http":  "http://{}:{}",
    "https": "https://{}:{}",
    "ftp":   "ftp://{}:{}"
}

url_body = "{}://icanhazip.com/"
try:
    ip,port,kind = "192.41.71.221   3128  https".split()
    kind = kind.lower()
    url = url_body.format(kind)
    proxies = {kind: kind_D[kind].format(ip,port)}
    print(proxies)
    # proxies = {}

    req = requests.get(url, headers=headers, proxies=proxies, timeout=5)
    print(req.status_code)
    print(req.text)
except Exception as e:
    print(e)
