import requests
# headers={'X-Forwarded-For':'1.1.1.1'}
# r = requests.get(r'http://jsonip.com',headers=headers)
# proxies = {'http': 'http://50.233.137.34:80'}
# r = requests.get(r'http://jsonip.com',proxies=proxies)
# ip= r.json()['ip']
# print(ip)

# url_test = 'http://icanhazip.com'
# r = requests.get(url_test)
# print(r.text)

def getProxy():
    try:
        r = requests.get('http://127.0.0.1:5010/get/',timeout=2.0)
    except:
        print('Cannot getProxy!')
        return None
    else:
        return r.content

def delProxy(proxy):
    requests.get('http://127.0.0.1:5010/delete/?proxy={}'.format(proxy))
    print('Deleted!')

def getHtml():
    proxy = getProxy()
    if proxy is None:
        return
    proxy = str(proxy, encoding='utf8')
    proxies = {"http": "http://{}".format(proxy)}
    try:
        print('Trying: ',proxy)
        r = requests.get(url_test,proxies = proxies,timeout=3.0)
        print('Succeed at:', proxy)
    except:
        print('Failed!')
        delProxy(proxy)
    return None

if __name__ == '__main__':
    url_test = 'http://icanhazip.com'
    for i in range(1,11):
        getHtml()