from datetime import *
from time import *
from math import *
import requests
import json

class User():
    def __init__(self, mid_str, name_str, timestamp_str):
        self.mid = int(mid_str)
        self.timestamp_str = timestamp_str
        self.name = name_str
        self.timeFormat()
    def timeFormat(self):
        try:
            self.timestamp = int(self.timestamp_str)
        except:
            self.timestamp = self.timestamp_str
        else:
            self.timelocal = datetime.fromtimestamp(self.timestamp)
            self_day_str = self.timelocal.strftime('%Y%m%d')
            self.day = int(self_day_str)


def fetchUser(mid):
    sleep(0.5)
    url = 'https://space.bilibili.com/ajax/member/GetInfo'
    headers = {
        'Referer':'https://space.bilibili.com/'
    }
    data = {
        'mid':num2str(mid)
    }
    req_accepted = False
    while not req_accepted:
        try:
            req_info = requests.post(url,headers=headers,data=data)
            req_json = req_info.json()
            req_json_data = req_json.get('data')
            req_accepted = True
        except: # request is not accepted
            sleep(15)

    try:
        user_mid = req_json_data.get('mid')
    except: # mid does not exist
        print('User does not exist:', req_json_data.get('mid'))
        user_mid           = data.get('mid')
        user_timestamp = '----------'
        user_name      = '-'
    else:
        try:
            user_name = req_json_data.get('name')
            user_name = user_name.encode('gbk','ignore') # to discard special character
            user_name = user_name.decode('gbk')
        except: # name is invalid
            user_name = '-'

        try:
            user_timestamp = req_json_data.get('regtime')
            user_timelocal = datetime.fromtimestamp(user_timestamp)
        except: # the regtime is hidden
            user_timestamp = 'XXXXXXXXXX'
    user = User(user_mid, user_name, user_timestamp)
    return user


# mid_step_guess

def guessTargetMid(user1,user2,target_timestamp):
    if user1.mid > user2.mid:
        user_left = user2
        user_righ = user1
    else:
        user_left = user1
        user_righ = user2
    # if target_timestamp > user1.timestamp and target_timestamp > user2.timestamp:

    diff_mid = user_righ.mid - user_left.mid
    diff_timestamp = user_righ.timestamp - user_left.timestamp
    # if diff_timestamp == 0 ???
    diff_target = target_timestamp - user_righ.timestamp
    # Use Binary search will encounter less problems!
    # Do not use linear-lerp search!
    # Because timestamp is not always different, 
    #   especially when the mid is very large.
    # And binary search won't spend too more time.
    mid_step_lerp = floor(diff_mid/diff_timestamp*diff_target)

    global mid_step_guess
    if target_timestamp > user_righ.timestamp:
        mid_step_guess = max(mid_step_guess, mid_step_lerp)
        # reserved_user = user_righ, guess_user
    else:
        mid_step_guess = mid_step_lerp
        # reserved_user = guess_user
    mid_guess = user_righ.mid + mid_step_guess
    return mid_guess

def validateUser(user,step=1):
    is_valid = False
    while not is_valid:
        if isinstance(user.timestamp, str):
            user = fetchUser(user.mid + step)
        else:
            is_valid = True
    return user

# user_pool = read from file 
    # user_guess = fetchUser(mid_guess)
    # user_guess = validateUser(user_guess)

def initUserPool():
    global user_pool
    user_pool_file = open('user_pool.json','r')
    user_pool_str = user_pool_file.read()
    user_pool_file.close()
    user_pool_json = json.loads(user_pool_str)
    user_json_1 = user_pool_json[0]
    user_json_2 = user_pool_json[1]
    user1 = fetchUser(user1['mid'])
    user2 = fetchUser(user2['mid'])
    return user1, user2


# while guess not correct
def updateGuessRange(user_guess,target_timestamp):
    # checkGuess
    global user_pool
    if user_pool[0].mid > user_pool[1].mid:
        user_left = user_pool[1]
        user_righ = user_pool[0]
    else:
        user_left = user_pool[0]
        user_righ = user_pool[1]
    if user_guess.mid > user_righ.mid:
        user_pool[0] = user_righ
        user_pool[1] = user_guess
    else:
        if user_guess.timestamp > target_timestamp:
            user_pool[0] = user_guess
            user_pool[1] = user_left
        else:
            user_pool[0] = user_righ
            user_pool[1] = user_guess

def isGuessCorrect(user_guess):
    user_prev = fetchUser(user_guess.mid-1)
    user_prev = validateUser(user_prev)
    if user_prev.day < user_guess.day:
        return True
    else:
        return False


date_bgn = date(2009,6,24)
date_end = date(2018,3,28)
date_gap = date_end - date_bgn
day_remained = date_gap.days+1
day_mid_dict = {}

def isDayMidDictFull():
    if day_remained == 0:
        return True
    else:
        return False

def updateTargetTimestamp():
    global day_remained
    day_remained = day_remained - 1
    # 



def enumDays():
    global day_mid_dict
    for i in range(date_gap.days+1):
        day_tmp = date_bgn + timedelta(days=i)
        # day_tmp = day_tmp.timetuple()
        # day_tmp = mktime(day_tmp)
        day_str = '{:>04}{:>02}{:>02}'.format(str(day_tmp.year),str(day_tmp.month),str(day_tmp.day))
        day_mid_dict[day_str] = None

def updateDayMidDict():

def recordDayMidDict():

def recordUserPool():

def spider():


if __name__ == '__main__':
    initUserPool()


