# from test_proxies import *
import requests

url_test = 'http://icanhazip.com'

proxy = '111.178.233.26:8080'
proxies = {"http": "http://{}".format(proxy)}

r = requests.get(url_test,proxies = proxies,timeout=1.0)
# try:
#     print('Trying: ',proxy)
#     r = requests.get(url_test,proxies = proxies,timeout=1.0)
#     print('Succeed at:', proxy)
# except:
#     print('Failed!')