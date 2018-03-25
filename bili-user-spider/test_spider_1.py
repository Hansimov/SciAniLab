import requests
import datetime

# url_mem_card = 'https://api.bilibili.com/x/web-interface/card?mid=15870477'
mem_url = 'https://space.bilibili.com/ajax/member/GetInfo'

mem_headers = {
    # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
    # 'Content-Type':'application/x-www-form-urlencoded',
    'Referer':'https://space.bilibili.com/' 
    }

# The line of 'Referer' is necessary, or you will encounter the 'gbk' problem

mem_data = {
    'mid':'22'
}


# r= requests.get(url_mem_card)
mem_req = requests.post(mem_url,headers = mem_headers, data = mem_data)
# print(type(r.json()))
mem_json = mem_req.json()
mem_json_data = mem_json.get('data')


try:
    user_mid     = mem_json_data.get('mid')
except:
    print('User does not exist:', mem_data.get('mid'))
    # If the user is not existent, this line will cause this error:
    #   AttributeError: 'str' object has no attribute 'get'
else:
    user_name    = mem_json_data.get('name')
    user_regtime = mem_json_data.get('regtime')
    try:
        print(user_mid,user_name,(datetime.datetime.fromtimestamp(user_regtime)))
    except:
        print(user_mid, user_name,'XXX')
        

'''
There are two ways to represent the trends of increasing users
1. Time in uniform speed 
   - This one is more natural, but also needs more complex spider algorithms
2. mid in uniform speed
   - This one is easy, but unatural.
'''

'''
One method is to get all the mids and their info,
but this method takes too much time and space.

So I decide to use the method below:

1.  Calculate the time stamps of the beginning of each day 
    since the first user of Bilibili is registered.
2.  Collect the first several mids (maybe 100/sec) with small intervals
    and calculate the most possible user registered at the beginning that day 
    by curve fitting.
   
    I assume that the increase of the number is linear within one day.
    Interplolation search and block search may be used.
    Use regtime to locate the useful mid.

3.  Then use binary search among the possible mids 
    to determine the accurate mid of the first registered user on that day.
4.  What we need are: mid, name and regtime,
    others are not useful currently so we will discard them.
'''

