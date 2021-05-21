import collections
import datetime
import eventlet
eventlet.monkey_patch(thread=False)
import json
import os
import pickle
import random
import re
import requests
import shutil
# import socket
import sys
import threading
import time

t0 = time.time()

""" Global variables """
mid = 546195 # 老番茄
root = "./ups/mid-{}/".format(mid)

""" Assitant functions """

def headers():
    return { "user-agent": "botnet - {}".format(random.random()) }

def join_path(*args):
    return os.path.join(*args).replace("\\","/")

def dt2ct(dt):
    return datetime.datetime.timestamp(dt)

def ct2dt(ct):
    return datetime.datetime.fromtimestamp(ct)

def dt2str(dt):
    return dt.strftime("%Y-%m-%d-%H-%M-%S")

def dt2dt0(dt,hour=0):
    return datetime.datetime(dt.year,dt.month,dt.day,hour,0,0)

def ct2dt0(ct):
    return dt2dt0(ct2dt(ct))

V_TABLE="fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF"
V_MAP={}
for i in range(58):
    V_MAP[V_TABLE[i]]=i
V_OFFSET=[11,10,3,8,4,6]
V_ADD, V_XOR = 8728348608, 177451812

def bv2av(bv_str):
    """ return av_int """
    # http://api.bilibili.com/x/web-interface/archive/stat?bvid={}
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

def req_get(url,headers={},proxies={},timeout=10.0, sleep=0.3):
    status_code = -1
    while status_code != 200:
        try:
            with eventlet.Timeout(timeout):
                req = requests.get(url,headers=headers, proxies=proxies)
        except:
            print("x retry!")
            time.sleep(sleep)
            continue
        status_code = req.status_code
    return req

def is_any_thread_alive(thread_L):
    return True in [t.is_alive() for t in thread_L]

""" Fetch vlist
# func:  fetch_vlist(mid)
# retn:  ---
# dump:  "./ups/mid-{mid}/infos/vlist.json"
"""

info_path = root+"infos/"
vlist_fname = info_path+"vlist.json"

def fetch_vpage(mid, page, pagesize=100):
    av_url_body = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid={}&page={}&pagesize={}"
    print("> Fetching mid {} page {}".format(mid,page))
    req  = req_get(av_url_body.format(mid,page,pagesize), headers=headers(), timeout=4.0, sleep=0.3)
    data = req.json()
    page_num = data["data"]["pages"]
    return data, page_num

def fetch_vlist(mid=mid):
    page, pagesize = 1, 100
    jsn, page_num = fetch_vpage(mid, page,pagesize)

    for i in range(2, page_num+1):
        time.sleep(0.4)
        tmp_jsn, _ = fetch_vpage(mid,i,pagesize)
        jsn["data"]["vlist"].extend(tmp_jsn["data"]["vlist"])

    if not os.path.exists(info_path):
        os.mkdir(info_path)
    with open(vlist_fname, mode="w", encoding="utf-8") as wf:
        data = jsn["data"]
        json.dump(jsn["data"], wf)

# fetch_vlist(mid)

""" Parse vlist
# func:  parse_vlist(mid), fetch_covers()
# retn:  ---
# open:  "./ups/mid-{}/infos/vlist.json"
# dump:  "./ups/mid-{}/infos/vinfo.pkl"
         vinfo_L: list of dict (video_num x col_num)
            each row: {aid: *, created: *, title: *, pic_url: *, length: *}
            sorted by aid
"""

vinfo_fname = info_path+"vinfo.pkl"

def parse_vlist():
    with open(vlist_fname, mode="r", encoding="utf-8") as rf:
        data = json.load(rf)
    vinfo_L = []
    cover_L = []
    for i,video in enumerate(data["vlist"]):
        # print("{:>3}/{} {:<10} {}  {}".format(i+1,len(data["vlist"]),video["aid"], datetime.datetime.fromtimestamp(int(video["created"])), video["title"]))
        vinfo_D = {}
        for key in ["aid", "title","created","length","pic"]:
            vinfo_D[key] = video[key]
        vinfo_L.append(vinfo_D)

    vinfo_L = sorted(vinfo_L, key=lambda k:k["created"])
    for i,video in enumerate(vinfo_L):
        print("{:>3}/{} {:>10} {}  {}".format(i+1,len(vinfo_L), video["aid"], datetime.datetime.fromtimestamp(int(video["created"])), video["title"]))
    with open(vinfo_fname, "wb") as wf:
        pickle.dump(vinfo_L, wf)

# parse_vlist(mid)

cover_path = root+"covers/"
def fetch_covers():
    if not os.path.exists(cover_path):
        os.makedirs(cover_path)
    with open(vlist_fname, "r", encoding="utf-8") as rf:
        data = json.load(rf)
        pic_L = []
        for video in data["vlist"][:]:
            aid, url, title = [video["aid"], "http:"+video["pic"], video["title"]]
            pic_L.append([aid, url, title])

        start = 0
        for i,pic in enumerate(pic_L[start:]):
            aid, url, title = pic
            print("{:>3}/{} {}: {}".format(start+i+1,len(pic_L),aid,title))
            req = req_get(url, headers=headers(), timeout=6.0)

            name,ext = os.path.splitext(url)
            img_name = "{}{}".format(aid,ext)
            with open(join_path(cover_path,img_name), "wb") as wf:
                wf.write(req.content)

            if ext != ".jpg":
                jpg_name = "{}.jpg".format(aid)
                os.system("magick convert \"{}\" \"{}\"".format(cover_path+img_name, cover_path+jpg_name))

# fetch_covers()


""" Fetch replies
# func:  fetch_replies()
# retn:  ---
# open:  "./infos/{mid}-vinfo.pkl"
# save:  "./replies/mid-{mid}/aid-{*}/reply-{*}-{size}.json"
"""

reply_url_next = "http://api.bilibili.com/x/v2/reply/main?oid={}&type=1&mode=2&next={}&ps={}"
reply_url_prev = "http://api.bilibili.com/x/v2/reply/main?oid={}&type=1&mode=2&prev={}&ps={}"

reply_path_body = root+"replies/aid-{:0>12}/"
floor_margin = 1000
video_cnt, total_video_cnt = -1, -1

def fetch_floors(aid,prev_floor=0,ps=1,video_cnt=-1,proxies={}):
    print("> {:>3}/{:>3} aid={:<10} prev={:<7} ps={:<4}".format(video_cnt, total_video_cnt,aid,prev_floor,ps))
    reply_path = reply_path_body.format(aid)

    t1 = time.time()
    if prev_floor==0:
        flr_fname = "reply-{:0>6}-{:0>4}.json".format(prev_floor,floor_margin)
    else:
        flr_fname = "reply-{:0>6}-{:0>4}.json".format(prev_floor,ps)

    if prev_floor == 0:
        req = req_get(reply_url_next.format(aid,floor_margin,floor_margin), headers=headers(), timeout=4.0, sleep=0.5)
    else:
        req = req_get(reply_url_prev.format(aid,prev_floor,ps), headers=headers(), timeout=4.0, sleep=0.5)

    t2 = time.time()

    status_flag = "+++" if req.status_code==200 else "xxx"
    print("{} {}  {}s".format(status_flag, req.status_code, round(t2-t1,1)))

    jsn = json.loads(req.content.decode("utf-8"))

    # Here often occurs: Keyerror: 'data' ...
    # Restart (several trials) the program solves it.
    # Still don't know why. Maybe the issue of home network.

    if not jsn["data"]["cursor"]["is_begin"]:
        with open(reply_path+flr_fname, "wb") as wf:
            wf.write(req.content)

    finfo_L = []
    for key in ["all_count","prev","next","is_begin","is_end"]:
        finfo_L.append(jsn["data"]["cursor"][key])

    return finfo_L

def fetch_replies(aid, is_overwrite=False, fetch_replies_sema=None, video_cnt=-1,proxies={}):
    if fetch_replies_sema:
        fetch_replies_sema.acquire()

    reply_path = reply_path_body.format(aid)
    if not os.path.exists(reply_path):
        os.makedirs(reply_path)

    old_prev_floor = 0
    page_floor_size = 1000

    if os.listdir(reply_path) == []:
        pass
    else:
        if is_overwrite or len(os.listdir(reply_path))<=1:
            shutil.rmtree(reply_path)
            os.makedirs(reply_path)
        else:
            # print(os.listdir(reply_path))
            os.remove(reply_path+os.listdir(reply_path)[-1])
            last_filename = os.listdir(reply_path)[-1]
            with open(reply_path+last_filename,mode="r",encoding="utf-8") as rf:
                jsn = json.load(rf)
            old_prev_floor = jsn["data"]["cursor"]["prev"]

    all_count, new_prev_floor, next_floor, is_begin, is_end = fetch_floors(aid, old_prev_floor,page_floor_size,video_cnt,proxies)

    # max_floor = 3500
    # while not (is_begin or new_prev_floor==old_prev_floor or new_prev_floor > max_floor):
    while not (is_begin or new_prev_floor==old_prev_floor):
        old_prev_floor = new_prev_floor
        time.sleep(0.2)
        all_count, new_prev_floor, next_floor, is_begin, is_end = fetch_floors(aid,new_prev_floor,page_floor_size,video_cnt,proxies)

    if fetch_replies_sema:
        fetch_replies_sema.release()

def fetch_all_video_replies(is_overwrite=False):
    global total_video_cnt
    with open(vinfo_fname, "rb") as rf:
        video_L = pickle.load(rf)

    total_video_cnt = len(video_L)
    start_cnt = 0
    # for i, video in enumerate(reversed(video_L)[start_cnt:]):
    for i, video in enumerate(video_L[start_cnt:]):
        video_cnt = start_cnt+i+1
        t1 = time.time()
        print("Fetching  aid={:<10} {}".format(video["aid"], video["title"]))
        fetch_replies(video["aid"],is_overwrite=is_overwrite,video_cnt=video_cnt)
        t2 = time.time()
        print("=== {:>3}/{:>3} Elapsed time: {}s".format(video_cnt, total_video_cnt, round(t2-t1,1)))

# fetch_all_video_replies()

def fetch_all_video_replies_multi(video_L,is_overwrite=False):
    global video_cnt, total_video_cnt
    total_video_cnt = len(video_L)

    fetch_replies_sema = threading.BoundedSemaphore(5)

    start_cnt = 0
    thread_L = []
    for i, video in enumerate(video_L[start_cnt:]):
        video_cnt = start_cnt+i+1
        tmp_thread = threading.Thread(target=fetch_replies,args=(video["aid"],False,fetch_replies_sema,video_cnt))
        thread_L.append(tmp_thread)
    for tmp_thread in thread_L:
        tmp_thread.start()

    while is_any_thread_alive(thread_L):
        time.sleep(0)

""" Parse replies
# func:  parse_replies()
# retn:  ---
# open:  "./ups/mid-{mid}/replies/aid-{*}/reply-{*}-{size}.json"
# dump:  "./ups/mid-{mid}/infos/finfo.pkl"
         finfo_D: dict of list (1 x video_num)
            each key,val: {aid: flr_ct_L}
                flr_ct_L: 2d list (flr_num x 2)
                    each row: [flr_idx, ctime]
                        flr_num: total num of all floors
                        flr_idx: index of current floor
                        ctime:   timestamp of floor
"""

finfo_fname = info_path+"finfo.pkl"

def parse_replies():
    reply_root = root+"replies/"
    finfo_D = {}
    t0 = time.time()
    folder_L = os.listdir(reply_root)[:]
    for i,folder in enumerate(folder_L):
        t1 = time.time()
        aid = int(re.findall(r"aid-(\d+)",folder)[0])
        finfo_L = []
        for fname in os.listdir(reply_root+folder)[:]:
            with open(join_path(reply_root,folder,fname),"r",encoding="utf-8") as rf:
                jsn = json.load(rf)
                for reply in jsn["data"]["replies"]:
                    finfo_L.append([reply["floor"],reply["ctime"]])
        finfo_L = sorted(finfo_L, key=lambda v:v[0])
        finfo_D[aid]= finfo_L
        print("{:>3}/{:<3} | {:<10} {:<6} | {}s".format(i+1, len(folder_L), aid, len(finfo_L), round(time.time()-t1,1)))

    with open(finfo_fname, "wb") as wf:
        pickle.dump(finfo_D, wf)
    print("Total elapsed time: {}s".format(round(time.time()-t0,1)))

# parse_replies(mid)

""" Calc accumulative floor count
# func:  calc_accum_flr_cnt()
# retn:  ---
# open:  "./ups/mid-{mid}/infos/finfo.pkl"
# dump:  "./ups/mid-{mid}/infos/tinfo.pkl", "./ups/mid-{mid}/infos/ninfo.pkl"
        ct_L(tinfo): list of ctime (1 x ct_group_cnt)
        ninfo_L: 2d list (video_num x ct_group_cnt)
            each row: list of accumulate floor count of all ctime groups
"""

tinfo_fname = info_path+"tinfo.pkl"

def create_ct_list(day_divi=3):
    with open(vinfo_fname, "rb") as rf:
        vinfo_L = pickle.load(rf)

    date_L = []
    start_ct = vinfo_L[0]["created"]
    end_ct = time.time()
    start_dt0 = ct2dt0(start_ct)
    end_dt0 = ct2dt0(end_ct)+datetime.timedelta(days=1)

    delta_days = (end_dt0 - start_dt0).days

    hour_L = [i*(24//day_divi) for i in range(day_divi)]

    ct_L = []
    for i in range(delta_days+1):
        tmp_dt = start_dt0+datetime.timedelta(days=i)
        for hour in hour_L:
            ct_L.append(dt2ct(dt2dt0(tmp_dt,hour)))
    with open(tinfo_fname,"wb") as wf:
        pickle.dump(ct_L, wf)

ninfo_fname = info_path+"ninfo.pkl"
def calc_accum_flr_cnt():
    with open(vinfo_fname, "rb") as rf:
        vinfo_L = pickle.load(rf)
    with open(finfo_fname, "rb") as rf:
        finfo_D = pickle.load(rf)
    with open(tinfo_fname, "rb") as rf:
        ct_L = pickle.load(rf)

    ninfo_L = []
    for i,vinfo in enumerate(vinfo_L):
        finfo = finfo_D[vinfo["aid"]]
        fp = 0
        print("{:>3}/{} calc accum flr cnt of {}".format(i+1,len(vinfo_L),vinfo["title"]))

        accum_flr_cnt = 0
        accum_flr_cnt_L = []
        for j,ct in enumerate(ct_L[:]):
            while fp < len(finfo) and finfo[fp][1] < ct_L[j]:
                accum_flr_cnt = finfo[fp][0]
                fp += 1
            accum_flr_cnt_L.append(accum_flr_cnt)
        ninfo_L.append(accum_flr_cnt_L)
    with open(ninfo_fname, "wb") as wf:
        pickle.dump(ninfo_L, wf)


""" Sort accumulated floor counts with ctime
# func:  sort_accum_flr_cnt(mid)
# retn:  ---
# open:  "./infos/{mid}-tinfo.pkl", "./infos/{mid}-ninfo.pkl"
# dump:  "./infos/{mid}-sinfo.pkl"
         sinfo: 2d list (ct_group_cnt x k)
            each row: list (1 x k), top k aids ranked by accumulated floor nums at each ctime group
"""

sinfo_fname = info_path+"sinfo.pkl"
def sort_accum_flr_cnt(topk=20):
    with open(vinfo_fname, "rb") as rf:
        vinfo_L = pickle.load(rf)
    with open(ninfo_fname, "rb") as rf:
        ninfo_L = pickle.load(rf)
    with open(tinfo_fname, "rb") as rf:
        ct_L = pickle.load(rf)
    
    sorted_idx_col_L = []
    for i in range(len(ct_L)):
        col = [row[i] for row in ninfo_L]
        sorted_idx_col = sorted(range(len(col)), key=lambda k: col[k], reverse=True)
        sorted_idx_col_L.append(sorted_idx_col[:topk])
        # sorted_idx_col_L.extend(sorted_idx_col[:1]) # use this to counter

    # print(sorted_idx_col_L[-10])
    # print([row[-1] for row in ninfo_L])
    # counter = collections.Counter(sorted_idx_col_L)
    # counter = {k: v for k, v in sorted(counter.items(), key=lambda item: item[1], reverse=True)}
    # for key,val in counter.items():
    #     print("{:>4}".format(val), vinfo_L[key][3])
    # print(counter)
    with open(sinfo_fname,"wb") as wf:
        pickle.dump(sorted_idx_col_L, wf)

""" [Not in this file] Animation """

if __name__ == '__main__':
    pass
    # fetch_vlist()
    # parse_vlist()
    # fetch_covers()
    # fetch_all_video_replies()
    # parse_replies()
    # create_ct_list(day_divi=3)
    # calc_accum_flr_cnt()
    # sort_accum_flr_cnt()
    print("Total elapsed time: {}s".format(round(time.time()-t0,1)))

