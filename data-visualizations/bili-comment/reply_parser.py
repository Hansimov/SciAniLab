import os
import sys
import json
import random
import datetime
import time
import re
import collections
import pickle
import requests
from matplotlib import pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei'] # 正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False   # 正常显示负号
# import numpy as np
import eventlet
eventlet.monkey_patch(thread=False)


def headers():
    return { "user-agent": "botnet - {}".format(random.random()) }

# 2013.10.05 -> 2020.05.05 = 2404 (days)
# print((datetime.date(2020,5,5)-datetime.date(2013,10,5)).days)
# 2404/30*3 ~ 240(s) = 4(min)
# floors num per day (every 8 hours)

# 2404 * 3 * 293
# hour: 00-07, 08-15, 16-23
# heat = current_window_weighted_floor_num
# aid, created, title, total_floor_num, new_add_floor_num, heat, img
# may be used later: hots, tags, plays, likes, coins, favorites
# current_window_floors_L = 293 * 2403 * 3

# cover animation: heat, aid, created, title,
# newest video: aid, created, title, img
# curve: heat

# use p5py

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


def parse_reply_info():
    up_mid = 546195
    root = "./mid-{}/".format(up_mid)
    rinfo_D = {}
    t0 = time.time()
    folder_L = os.listdir(root)[:]
    for i,folder in enumerate(folder_L):
        t1 = time.time()
        oid = int(re.findall(r"oid-(\d+)",folder)[0])
        finfo_L = []
        for file in os.listdir(root+folder)[:]:
            # print(file)
            with open(join_path(root,folder,file),"r",encoding="utf-8") as rf:
                data = json.load(rf)
                for reply in data["data"]["replies"]:
                    finfo_L.append([reply["floor"],reply["ctime"]])
        finfo_L = sorted(finfo_L, key=lambda v:v[0])
        rinfo_D[oid]= finfo_L
        print("{:>3}/{:<3} | {:<10} {:<6} | {}s".format(i+1, len(folder_L), oid, len(finfo_L), round(time.time()-t1,1)))
    with open("rinfo.pkl", "wb") as wf:
        pickle.dump(rinfo_D, wf)
    print("Total elapsed time: {}s".format(round(time.time()-t0,1)))


def parse_vlist_info():
    vinfo_L = []
    vlist_file = "vlist.json"
    with open(vlist_file,"r",encoding="utf-8") as rf:
        data_L = json.load(rf)
        for data in data_L[:]:
            for video in data["data"]["vlist"][:]:
                vinfo = [video["aid"],video["created"],video["length"],video["title"]]
                vinfo_L.append(vinfo)

    vinfo_L = sorted(vinfo_L,key=lambda v:v[1])

    for i,vinfo in enumerate(vinfo_L):
        print(ct2dt(vinfo[1]), vinfo)
    with open("vinfo.pkl","wb") as wf:
        pickle.dump(vinfo_L, wf)


def load_info():
    # list of [aid,created,length,title]
    with open("vinfo.pkl", "rb") as rf:
        vinfo_L = pickle.load(rf)
    # # dict of {oid: list of [floor,ctime]}
    with open("rinfo.pkl", "rb") as rf:
        rinfo_D = pickle.load(rf)
    return vinfo_L, rinfo_D

def get_col(list_2d, col_num):
    return [row[col_num] for row in list_2d]

plot_path = "./plots/"
if not os.path.exists(plot_path):
    os.mkdir(plot_path)

def fetch_covers():
    vlist_file = "vlist.json"
    cover_path = "./covers/"
    if not os.path.exists(cover_path):
        os.mkdir(cover_path)
    with open(vlist_file,"r",encoding="utf-8") as rf:
        data_L = json.load(rf)
        pic_L = []
        for data in data_L[:]:
            for video in data["data"]["vlist"][:]:
                aid, url, title = [video["aid"], video["pic"], video["title"]]
                pic_L.append([aid, "http:"+url, title])

        start = 200
        for i,pic in enumerate(pic_L[start:]):
            aid, url, title = pic
            print("{:>3}/{} {}: {}".format(start+i+1,len(pic_L),aid,title))
            status_code = -1
            while status_code != 200:
                try:
                    with eventlet.Timeout(3.0):
                        req = requests.get(url, headers=headers())
                        status_code = req.status_code
                except:
                    print("xxx")
                    time.sleep(0.1)
            # time.sleep(0)
            _,ext = os.path.splitext(url)
            with open(join_path(cover_path,"{}{}".format(aid,ext)), "wb") as wf:
                wf.write(req.content)

    # for aid_pic in pic_L:
    #     print(aid_pic[0],aid_pic[1])

def customize_plt(title="",xlabel="",ylabel="",grid=False,size=None,tight_layout=False,cla=False,save_path=None, show=False):
    if size:
        fig = plt.gcf()
        mydpi = 100
        fig.set_size_inches((size[0]/mydpi,size[1]/mydpi))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if grid:
        plt.grid(True)
    if tight_layout:
        plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    if cla:
        plt.cla()
    if show:
        plt.show()

def plot_replies():
    # pass
    vinfo_L, rinfo_D = load_info()

    mydpi = 96
    fig = plt.figure(figsize=(1280/mydpi,720/mydpi),dpi=mydpi)
    for i,vinfo in enumerate(vinfo_L[:]):
        # vinfo: [aid, created, length, title]
        oid, created, _, title = vinfo
        print("{:>3}/{} {}".format(i+1, len(vinfo_L),title))
        rinfo = rinfo_D[oid]
        # calc_heat(rinfo)
        floor_L = get_col(rinfo,0)
        ctime_L = get_col(rinfo,1)
        dtime_L = list(map(ct2dt,ctime_L))
        # plt.plot(ctime_L,floor_L)
        plt.plot(dtime_L,floor_L)
        # plt.title("{}\n{}".format(title,ct2dt(created)))
        # plt.xlabel("时间")
        # plt.ylabel("评论数")
        # plt.grid(True)
        # plt.tight_layout()
        # plt.savefig(plot_path+"{:0>3}".format(i+1))
        # plt.cla()
        # plt.show()
        # # print(rinfo.__len__())
        # for reply in rinfo:
        #     print(reply[0], reply[1])
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(plot_path+"{:0>3}".format(0))


def create_ct_list(day_divi=3, vinfo_L=None, rinfo_D=None):
    if not vinfo_L or not rinfo_D:
        vinfo_L, rinfo_D = load_info()

    date_L = []
    start_ct = vinfo_L[0][1]
    end_ct = time.time()
    start_dt0 = ct2dt0(start_ct)
    end_dt0 = ct2dt0(end_ct)+datetime.timedelta(days=1)

    # print(start_dt0)
    # print(end_dt0)

    delta_days = (end_dt0 - start_dt0).days

    # day_divi = 3
    hour_L = [i*(24//day_divi) for i in range(day_divi)]

    dt_L = []
    ct_L = []
    # print(hour_L) # 0,8,16
    for i in range(delta_days+1):
        tmp_dt = start_dt0+datetime.timedelta(days=i)
        # print(new_dt)
        # tmp_dt 
        for hour in hour_L:
            # dt_L.append(dt2dt0(tmp_dt,hour))
            ct_L.append(dt2ct(dt2dt0(tmp_dt,hour)))
    return ct_L
    # print(len(ct_L))

def calc_heat():
    # vinfo: [aid, created, length, title]
    # rinfo: key=oid , val=list of [floor,ctime]
    vinfo_L, rinfo_D = load_info()

    ct_L = create_ct_list(3, vinfo_L, rinfo_D)
    heat_path = "./heats/"
    if not os.path.exists(heat_path):
        os.mkdir(heat_path)

    hinfo_L = []
    for i,vinfo in enumerate(vinfo_L[:]):
        oid, created, length, title = vinfo
        rinfo = rinfo_D[oid]
        heat_L = []
        r_p = 0
        print("{:>3}/{} heat of {}".format(i+1,len(vinfo_L),title))
        for j,ct in enumerate(ct_L[:-1]): # -1 here used to avoid i+1 overflow
            heat = 0
            while r_p < len(rinfo) and rinfo[r_p][1] >= ct and rinfo[r_p][1] < ct_L[j+1]:
                heat += 1
                r_p += 1
                # print(r_p,heat)
            # print(ct2dt(ct),heat)
            heat_L.append(heat)
        # print(len(heat_L))
        # tmp_ct_L = [row[0] for row in heat_L]
        # tmp_heat_L = [row[1] for row in heat_L]
        # plt.plot(tmp_ct_L, tmp_heat_L)
        # customize_plt(title="{}\n{}".format(title,ct2dt(created)),xlabel="时间",ylabel="评论数",grid=True,size=(1280,720),tight_layout=False,save_path=join_path(heat_path,"{:0>3}.png".format(i+1)))
        hinfo_L.append(heat_L)

        # print(len(hinfo_L))
    for heat_L in hinfo_L:
        plt.plot(list(map(ct2dt,ct_L[:-1])),heat_L)
        # plt.cla()
    customize_plt(grid=True,size=(1280,720), tight_layout=True, save_path=join_path(heat_path,"{:0>3}.png".format(0)))

    # with open("hinfo.pkl","wb") as wf:
    #     pickle.dump([ct_L[:-1], hinfo_L],wf)

def rank_heat():
    with open("hinfo.pkl","rb") as rf:
        ct_L, hinfo_L = pickle.load(rf)
    # print(len(ct_L), len(hinfo_L[0]))
    # plt.plot(ct_L,hinfo_L[30])
    # customize_plt(show=True)
    idx_LL = []
    for i in range(len(ct_L[:])):
    # i = len(ct_L[:-18])
        col = [row[i] for row in hinfo_L]
        # print(col)
        sorted_idx_L = sorted(range(len(col)), key=lambda k: col[k], reverse=True)
        # print(sorted_idx_L[0:4])
        if col[sorted_idx_L[0]] > 10:
            idx_LL.extend(sorted_idx_L[0:4])
    counter = collections.Counter(idx_LL)
    print(counter)


def calc_floor_num():
    vinfo_L, rinfo_D = load_info()

    ninfo_L = []
    ct_L = create_ct_list(3, vinfo_L, rinfo_D)
    for i,vinfo in enumerate(vinfo_L[:]):
        oid, created, length, title = vinfo
        rinfo = rinfo_D[oid]
        r_p = 0
        print("{:>3}/{} floor num of {}".format(i+1,len(vinfo_L),title))

        floor_num = 0
        floor_num_L = []
        for j,ct in enumerate(ct_L[:]): # -1 here used to avoid i+1 overflow
            while r_p < len(rinfo) and rinfo[r_p][1] < ct_L[j]:
                floor_num = rinfo[r_p][0]
                r_p += 1
                # print(r_p,heat)
            # print(ct2dt(ct),heat)
            floor_num_L.append(floor_num)
        ninfo_L.append(floor_num_L)
    # print(len(ninfo_L))
    with open("ninfo.pkl", "wb") as wf:
        pickle.dump([ct_L,ninfo_L], wf)

def rank_floor_num():
    # vinfo: [aid, created, length, title]
    # rinfo: key=oid , val=list of [floor,ctime]
    vinfo_L, rinfo_D = load_info()
    with open("ninfo.pkl", "rb") as rf:
        ct_L, ninfo_L = pickle.load(rf)
    
    # plt.plot(list(map(ct2dt,ct_L)),ninfo_L[-1])
    # plt.show()
    idx_LL = []
    for i in range(len(ct_L[:])):
        col = [row[i] for row in ninfo_L]
        # print(col)
        sorted_idx_L = sorted(range(len(col)), key=lambda k: col[k], reverse=True)
        # print(sorted_idx_L[0:4])
        # idx_LL.extend(sorted_idx_L[:2])
        idx_LL.append(sorted_idx_L[:20])
    # counter = collections.Counter(idx_LL)
    # counter = {k: v for k, v in sorted(counter.items(), key=lambda item: item[1], reverse=True)}

    # for key,val in counter.items():
    #     print("{:>4}".format(val), vinfo_L[key][3])
    # print(counter)
    with open("ninfo_rank.pkl","wb") as wf:
        pickle.dump([ct_L,ninfo_L,idx_LL], wf)


if __name__ == '__main__':
    pass
    t0 = time.time()
    # parse_reply_info()
    # parse_vlist_info()
    # plot_replies()
    # ct_L = create_ct_list()
    # print(len(ct_L))
    # calc_heat()
    # rank_heat()
    # fetch_covers()
    # calc_floor_num()
    # rank_floor_num()

    print("Total elapsed time: {}s".format(round(time.time()-t0,1)))