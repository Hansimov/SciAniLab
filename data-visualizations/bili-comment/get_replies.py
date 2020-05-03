import os
import re
import datetime
import time
import random
import requests

import sys
import socket
import threading
import pickle
import eventlet
eventlet.monkey_patch(thread=False)


# http://api.bilibili.com/x/web-interface/archive/stat?bvid={}
V_TABLE="fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF"
V_MAP={}
for i in range(58):
    V_MAP[V_TABLE[i]]=i
V_OFFSET=[11,10,3,8,4,6]
V_XOR = 177451812
V_ADD = 8728348608

def bv2av(bv_str):
    r=0
    for i in range(6):
        r+=V_MAP[bv_str[V_OFFSET[i]]]*58**i
    return (r-V_ADD)^V_XOR

def av2bv(av_int):
    av_int=(av_int^V_XOR)+V_ADD
    r=list("BV1  4 1 7  ")
    for i in range(6):
        r[V_OFFSET[i]]=V_TABLE[av_int//58**i%58]
    return "".join(r)

print(bv2av("BV1Ya4y1t7fw")) # 667592495
print(av2bv(667592495))      # BV1Ya4y1t7fw