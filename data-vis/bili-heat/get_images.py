# up 头像
# https://i0.hdslb.com/bfs/face/
# 视频封面
# https://i2.hdslb.com/bfs/archive/

import requests
import time
import threading
import random
import os.path
import json

import datetime

total_num = 0
remaining_num = 0

thrd_num_max = 50
semlock = threading.BoundedSemaphore(thrd_num_max)

def getImage(img_link, img_name, retry_count=0):
    global remaining_num, total_num

    if os.path.exists(img_name):
        print(f'=== Remaining: {remaining_num:{0}{5}}/{total_num:{0}{5}} ===')
        print(f'+++ Existed: {img_name}')
        remaining_num -= 1
        semlock.release()
        return

    try:
        print(f'>>> Getting image: {img_link}')
        img = requests.get(img_link)
    except Exception as exc:
        retry_count += 1
        if retry_count >= 5:
            print(f'--- Exceeded retry limits: {img_name}')
            semlock.release()
            return
        else:
            print(f'*** Retry {retry_count} times to get: {img_name} ...')
            getImage(img_link, img_name, retry_count)
    else:
        with open(img_name, 'wb') as img_file:
            img_file.write(img.content)
        print(f'+++ Successfully dumped: {img_name}')
        remaining_num -= 1
        print(f'=== Remaining: {remaining_num:{0}{5}}/{total_num:{0}{5}} ===')
        semlock.release()

def createThread(img_link, img_ext, xid, xtype):
    xid_name = ('mid', 'aid')[xtype=='pic']
    img_name = f'{xtype}/{xid_name}_{xid:{0}{10}}{img_ext}'

    semlock.acquire()
    thrd = threading.Thread(target=getImage, args=[img_link, img_name])

    return thrd

def startThread(thrd):
    # thrd.daemon = True
    thrd.start()
    # thrd.join()

pic_list = []
aid_list = []


def getInfoList():
    global pic_list, face_list
    global total_num, remaining_num

    with open('jsons/ao.json', encoding='utf8', mode='r') as f:
        videos = json.load(f)
        page_num = len(videos)
        for page_idx in range(page_num):
            video_num = len(videos[page_idx]['data']['vlist'])
            for video_idx in range(video_num):
                # print(videos[page_idx]['data']['vlist'][video_idx]['title'])
                pic_list.append(videos[page_idx]['data']['vlist'][video_idx]['pic'])
                aid_list.append(videos[page_idx]['data']['vlist'][video_idx]['aid'])

    total_num = len(pic_list)
    remaining_num = total_num

def getAllImages():
    pic_thrd_pool = []

    for i in range(len(pic_list)):
        pic_tmp = pic_list[i]
        aid_tmp = aid_list[i]

        pic_img_link = 'https:' + pic_tmp
        pic_img_ext = os.path.splitext(pic_tmp)[1]

        pic_thrd = createThread(pic_img_link, pic_img_ext, xid=aid_tmp, xtype='pic')
        startThread(pic_thrd)

if __name__ == '__main__':
    if not os.path.exists('pic'):
        os.mkdir('pic')

    getInfoList()
    getAllImages()