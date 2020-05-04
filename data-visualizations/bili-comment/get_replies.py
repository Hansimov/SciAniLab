import os
import re
import datetime
import time
import random
import requests
import shutil

import sys
import json
# import socket
# import threading
# import pickle
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
    """ return av_int """
    r=0
    for i in range(6):
        r+=V_MAP[bv_str[V_OFFSET[i]]]*58**i
    return (r-V_ADD)^V_XOR

def av2bv(av_int):
    """ return bv_str """
    av_int=(av_int^V_XOR)+V_ADD
    r=list("BV1  4 1 7  ")
    for i in range(6):
        r[V_OFFSET[i]]=V_TABLE[av_int//58**i%58]
    return "".join(r)

def headers():
    return { "user-agent": "botnet - {}".format(random.random()) }

# https://m.bilibili.com/video/av667592495
# http://api.bilibili.com/x/v2/reply?oid=667592495&pn=1&ps=49&type=1&nohot=1&sort=0
# url_body = "http://api.bilibili.com/x/v2/reply?pn={}&type=1&oid={}&nohot=1&sort=0"
# BV1Qx411J7ER <-> 13592834 傅里叶
# uid: 546195


reply_url_next = "http://api.bilibili.com/x/v2/reply/main?oid={}&type=1&mode=2&next={}&ps={}"
reply_url_prev = "http://api.bilibili.com/x/v2/reply/main?oid={}&type=1&mode=2&prev={}&ps={}"
# def fetch_first_valid_floor(oid):

reply_path_body = "./mid-546195/oid-{:0>12}/"
floor_margin = 1000
def fetch_floors(oid,prev_floor=0,ps=1):
    print("> Fetching floors ... oid={:<10} prev={:<7} ps={:<4}".format(oid,prev_floor,ps))
    reply_path = reply_path_body.format(oid)

    t1 = time.time()
    if prev_floor==0:
        filename = "reply-{:0>6}-{:0>4}.json".format(prev_floor,floor_margin)
    else:
        filename = "reply-{:0>6}-{:0>4}.json".format(prev_floor,ps)

    status_code = -1
    while status_code != 200:
        try:
            with eventlet.Timeout(5.0):
                if prev_floor == 0:
                    req = requests.get(reply_url_next.format(oid,floor_margin,floor_margin), headers=headers())
                else:
                    req = requests.get(reply_url_prev.format(oid,prev_floor,ps), headers=headers())
                status_code = req.status_code
        except:
            time.sleep(0.5)
            continue

    t2 = time.time()

    flag_200 = "+++" if req.status_code==200 else "xxx"
    print("{} {}  {}s".format(flag_200, req.status_code, round(t2-t1,1)))

    with open(reply_path+filename, "wb") as wf:
        wf.write(req.content)

    data = json.loads(req.content.decode("utf-8"))
    # print(*list(map(lambda i: data["data"]["cursor"][i], ["prev","next","is_begin","is_end"])))

    # is_begin, is_end = False, False
    # all_count, prev_floor, next_floor, is_begin, is_end
    reply_info_L = list(map(lambda i: data["data"]["cursor"][i], ["all_count","prev","next","is_begin","is_end"]))

    return reply_info_L

# is_begin = true: end statement, stop fetching
# is_end = true  : the floors before `next` value is deleted calculated new "next" pa
# all_count: total count of all level floors
def fetch_replies(oid,is_overwrite=True):
    reply_path = reply_path_body.format(oid)
    if not os.path.exists(reply_path):
        os.makedirs(reply_path)

    old_prev_floor = 0
    page_floor_size = 1000

    if os.listdir(reply_path) == []:
        pass
    else:
        if is_overwrite or len(os.listdir(reply_path))<=2:
            shutil.rmtree(reply_path)
            os.makedirs(reply_path)
        else:
            # print(os.listdir(reply_path))
            os.remove(reply_path+os.listdir(reply_path)[-1])
            last_filename = os.listdir(reply_path)[-1]
            with open(reply_path+last_filename,mode="r",encoding="utf-8") as rf:
                data = json.load(rf)
            old_prev_floor = data["data"]["cursor"]["prev"]

    all_count, new_prev_floor, next_floor, is_begin, is_end = fetch_floors(oid, old_prev_floor,page_floor_size)

    # print(all_count, new_prev_floor, next_floor, is_begin, is_end)
    # max_floor = 3500
    # while not (is_begin or new_prev_floor==old_prev_floor or new_prev_floor > max_floor):
    while not (is_begin or new_prev_floor==old_prev_floor):
        old_prev_floor = new_prev_floor
        time.sleep(0.5)
        all_count, new_prev_floor, next_floor, is_begin, is_end = fetch_floors(oid,new_prev_floor,page_floor_size)

def parse_reply_json():
    # filename = "./mid-546195/oid-000667592495/reply-0001000-1000.json"
    # filename = "./mid-546195/oid-000667592495/reply-0000000-0001.json"
    # filename = "./mid-546195/oid-000667592495/reply-0000000-1000.json"

    with open(filename,mode="r",encoding="utf-8") as rf:
        data = json.load(rf)

    # print(data.keys())
    # print(data["data"].keys())
    # print(len(data["data"]["replies"]))
    # print(data["data"]["replies"][0])
    # print(data["data"]["cursor"].keys())
    # print(data["data"]["cursor"]["prev"])
    # print(data["data"]["cursor"]["next"])
    # print(*list(map(lambda i: data["data"]["cursor"][i], ["prev","next","is_begin","is_end"])))
    all_count, prev_floor, next_floor, is_begin, is_end = list(map(lambda i: data["data"]["cursor"][i], ["all_count","prev","next","is_begin","is_end"]))
    # prev_floor = 
    print(all_count, prev_floor, next_floor, is_begin, is_end)


# https://api.bilibili.com/x/article/archives?ids=2,3,4 # Get pubdate
# http://space.bilibili.com/ajax/member/getSubmitVideos?mid=546195&page=1&pagesize=100
av_url_body = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid={}&page={}&pagesize={}'
# http://api.bilibili.com/x/space/arc/search?pn=2&ps=100&mid=546195
# av_url_body = "http://api.bilibili.com/x/space/arc/search?ps={}&pn={}&mid={}"


def fetch_av_page(mid,page,pagesize=100):
    print("> Fetching av page {}".format(page))
    req  = requests.get(av_url_body.format(mid,page,pagesize))
    data = req.json()
    page_num = data["data"]["pages"]
    return data, page_num


av_path = "./avs/"
av_list_json_filename = "laofanqie_av_list.json"
def fetch_upper_av_list(mid):
    page, pagesize = 1, 100
    data_L = []
    data, page_num = fetch_av_page(mid,page,pagesize)
    data_L.append(data)

    for i in range(2, page_num+1):
        time.sleep(0.5)
        data, _ = fetch_av_page(mid,i,pagesize)
        data_L.append(data)

    if not os.path.exists(av_path):
        os.mkdir(av_path)
    with open(av_path+av_list_json_filename, mode="w", encoding="utf-8") as wf:
        json.dump(data_L, wf)


def parse_av_list_json():
    with open(av_path+av_list_json_filename, mode="r", encoding="utf-8") as rf:
        data_L = json.load(rf)

    video_L = []
    cover_L = []
    for data in data_L:
        for video in data["data"]["vlist"]:
            # print("{:<10} {}  {}".format(video["aid"], datetime.datetime.fromtimestamp(int(video["created"])), video["title"]))
            video_info_D = {}
            for key in ["aid","title","created","length","pic","play","favorites","comment"]:
                video_info_D[key] = video[key]
            video_L.append(video_info_D)
    return video_L

if __name__ == '__main__':

    t0 = time.time()
    # parse_reply_json()
    # fetch_replies(667592495)
    # fetch_upper_av_list(546195)
    video_L = parse_av_list_json()
    for video in video_L[:1]:
        t1 = time.time()
        print("Fetching  oid={:<10} {}".format(video["aid"], video["title"]))
        fetch_replies(video["aid"],is_overwrite=False)
        t2 = time.time()
        print("Elapsed time: {}s".format(round(t2-t1,1)))

    t3 = time.time()
    print("Total elapsed time: {}s".format(round(t3-t0,1)))