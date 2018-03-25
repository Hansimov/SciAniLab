import requests
import re
from datetime import *
from time import *

def getUserInfo(mem_data):
    try:
        mem_req = requests.post(mem_url,headers = mem_headers, data = mem_data)
        mem_json = mem_req.json()
        mem_json_data = mem_json.get('data')
    except: # requests error
        user_mid            = mem_data.get('mid')
        user_regtime_local  = '******** **********'
        user_regtime_stamp  = '**********'
        user_name           = '*'
    else:
        try:
            user_mid           = mem_json_data.get('mid')
        except: # the mid is not existent
            user_mid           = mem_data.get('mid')
            user_regtime_local = '-------- ----------'
            user_regtime_stamp = '----------'
            user_name          = '-'
        else:
            try: # name is valid
                user_name = mem_json_data.get('name')
                user_name = user_name.encode('gbk','ignore') # to discard special character
                user_name = user_name.decode('gbk')
            except:
                user_name = '-'

            try:
                user_regtime_stamp = mem_json_data.get('regtime')
                user_regtime_local = datetime.fromtimestamp(user_regtime_stamp)
            except: # the regtime is hidden
                user_regtime_local = 'XXXX-XX-XX XX:XX:XX'
                user_regtime_stamp = 'XXXXXXXXXX'
    return user_mid, user_regtime_local, user_regtime_stamp, user_name

def printUserInfo(user_mid, user_regtime_local, user_regtime_stamp, user_name):
    print('{:0>10s} {} {} {}'.format(user_mid, user_regtime_local, user_regtime_stamp, user_name))
    print('{:0>10s} {} {} {}'.format(user_mid, user_regtime_local, user_regtime_stamp, user_name),file=file_user_info)
    file_user_info.truncate()

def updateLatestMid(i):
    file_latest_mid.seek(0)
    print(i+1,file=file_latest_mid)
    file_latest_mid.truncate()

if __name__ == "__main__":
    file_user_info = open('user_info_test.txt','w+')
    file_latest_mid = open('latest_mid.txt','r+')

    latest_mid = int(file_latest_mid.read())

    mem_url = 'https://space.bilibili.com/ajax/member/GetInfo'
    mem_headers = {
        'Referer':'https://space.bilibili.com/' 
        }

    for i in range(15870470,15870488):
        mem_data = {
            'mid':str(i)
        }
        user_mid, user_regtime_local, user_regtime_stamp, user_name = getUserInfo(mem_data)
        printUserInfo(user_mid, user_regtime_local, user_regtime_stamp, user_name)
        updateLatestMid(i)
        sleep(0.5)



