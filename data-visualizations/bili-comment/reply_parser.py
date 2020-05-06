import os
import sys
import json
import datetime
import time
import re
import collections
import pickle


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

def ct2dt(ctime):
    return datetime.datetime.fromtimestamp(ctime)

def dt2str(dt):
    return dt.strftime("%Y-%m-%d-%H-%M-%S")


up_mid = 546195
root = "./mid-{}/".format(up_mid)

def parse_reply_info():
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
        rinfo_D[oid]= finfo_L
        print("{:>3}/{:<3} | {:<10} {:<6} | {}s".format(i+1, len(folder_L), oid, len(finfo_L), round(time.time()-t1,1)))
    with open(join_path(root,"rinfo.pkl"), "wb") as wf:
        pickle.dump(rinfo_D, wf)
    print("Total elapsed time: {}s".format(round(time.time()-t0,1)))


def parse_vlist_info():
    vinfo_L = []
    vlist_file = "vlist.json"
    # print(vlist_file)
    with open(vlist_file,"r",encoding="utf-8") as rf:
        data_L = json.load(rf)
        # print(data_L.__len__())
        for data in data_L[:]:
            # print(data["data"].keys())
            # print(data["data"]["vlist"].__len__())
            # print(data["data"]["vlist"][0].keys())
            for video in data["data"]["vlist"][:]:
                # print(video["title"])
                vinfo = [video["aid"],video["created"],video["length"],video["title"]]
                vinfo_L.append(vinfo)

    vinfo_L = sorted(vinfo_L,key=lambda v:v[1])

    for i,vinfo in enumerate(vinfo_L):
        print(ct2dt(vinfo[1]), vinfo)
    with open("vinfo.pkl","wb") as wf:
        pickle.dump(vinfo_L, wf)

# dict of list of [floor,ctime] pairs
with open("rinfo.pkl", "rb") as rf:
    rinfo_D = pickle.load(rf)
# list of [aid,created,length,title]
with open("vinfo.pkl", "rb") as rf:
    vinfo_L = pickle.load(rf)

# for vinfo in vinfo_L:
#     aid = vinfo[0]
#     print(aid, len(rinfo_D[aid]))

def calc_video_heat(oid):



if __name__ == '__main__':
    pass
    # parse_vlist_info()
    # parse_reply_info()