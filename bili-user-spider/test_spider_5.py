from datetime import *
from time import *
from math import *
import requests
import json

# Use log file to record variables,
#   instead of global variables read from files
# Because updating the file which stores global variables 
#   still has the risk of overwriting the file
#   and destroys it.

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
            self.timelocal = 'XXXX-XX-XX XX:XX:XX'
            self.day_str = 'XXXXXXXX'
            self.day = 10000000
        else:
            self.timelocal = datetime.fromtimestamp(self.timestamp)
            self_day_str = self.timelocal.strftime('%Y%m%d')
            self.day = int(self_day_str)

def fetchUser(mid):
    global invalid_mids, fetch_count

    if mid in invalid_mids:
        printLog('{} {:0>10d}'.format('--- Invalid mid:',mid))
        user_mid = str(mid)
        user_name = '-'
        user_timestamp = '----------'
        user = User(user_mid, user_name, user_timestamp)
        return user

    fetch_count += 1
    # if fetch_count >= 180:
    #     printLog('*** Sleep for a long time ***')
    #     for i in range(1,10):
    #         printLog('  *** Sleep {} seconds ...'.format(i*10))
    #         sleep(10)
    #     fetch_count = 0

    sleep(0.25)

    url = 'https://space.bilibili.com/ajax/member/GetInfo'
    headers = {
        'Referer':'https://space.bilibili.com/'
    }
    mid_str = str(mid)
    data = {
        'mid':mid_str
    }
    is_mid_valid = False
    req_accepted = False
    while not req_accepted:
        printLog('{} {:0>10s}'.format('>>> Fetching :', mid_str))
        try:
            req_info = requests.post(url,headers=headers,data=data)
            req_json = req_info.json()
            req_json_data = req_json.get('data')
            req_accepted = True
        except: # request is not accepted
            printLog('{} {:0>10s}'.format('--- Request denied, retry:',mid_str))
            if fetch_count != 0:
                printLog('[fetch_count: {}]'.format(fetch_count))
                fetch_count = 0
            sleep(10)

    try:
        user_mid = req_json_data.get('mid')
    except: # mid does not exist
        printLog('{} {:0>10s}'.format('--- User does not exist:',mid_str))
        user_mid           = data.get('mid')
        user_timestamp = '----------'
        user_name      = '-'
    else:
        try:
            user_name = req_json_data.get('name')
            user_name = user_name.encode('gbk','ignore') # to discard special character
            user_name = user_name.decode('gbk')
        except: # name is invalid
            printLog('{} {:0>10s}'.format('--- Name is invalid:',mid_str))
            user_name = '-'

        try:
            user_timestamp = req_json_data.get('regtime')
            user_timelocal = datetime.fromtimestamp(user_timestamp)
        except: # the regtime is hidden
            printLog('{} {:0>10s}'.format('--- Regtime is hidden:',mid_str))
            user_timestamp = 'XXXXXXXXXX'
        else:
            is_mid_valid = True

    if not is_mid_valid:
        invalid_mids.append(mid)
        printLog('[{} {}]'.format('Number of invalid mids:',len(invalid_mids)))

    user = User(user_mid, user_name, user_timestamp)
    userstr = '{:0>10s} {} {} {}'.format(user_mid, user_timestamp,user.timelocal,user_name)
    printLog(userstr)
    return user

def guessMid():
    global user_left, user_righ, target_day, guess_step, guess_mid, invalid_mids, guessed_mids

    # if len(invalid_mids) >= 50:
    #     is_today_has_user = -1
    #     return is_today_has_user

    is_today_has_user = 1

    if user_righ.day < target_day:
        guess_step = 8 * max(guess_step, user_righ.mid - user_left.mid)
        guess_mid = user_righ.mid + guess_step
    else:
        guess_mid = floor((user_left.mid + user_righ.mid)/2)

    orient = 1
    while (guess_mid in invalid_mids) or (guess_mid in guessed_mids):
        # if (guess_mid>=user_left.mid) and (guess_mid<=user_righ.mid):
        guess_mid = guess_mid + orient
        if guess_mid > user_righ.mid:
            orient = -1
            guess_mid = guess_mid + orient
        elif guess_mid < user_left.mid:
            is_today_has_user = 0
            break

    guessed_mids.append(guess_mid)

    printLog('[{} {} ~ {} {}]'.format('guess_mid:',guess_mid,'target_day',target_day))

    return is_today_has_user


def updateGuessRange(guess_user):
    global user_left, user_righ, target_day
    if user_righ.day < target_day:
        user_left = user_righ
        user_righ = guess_user
    else:
        if guess_user.day < target_day:
            user_left = guess_user
            user_righ = user_righ
        else:
            user_left = user_left
            user_righ = guess_user

def validateUser(user,step=1):
    is_valid = False
    while not is_valid:
        if isinstance(user.timestamp, str):
            user = fetchUser(user.mid + step)
        else:
            is_valid = True
    return user

def isGuessCorrect(guess_user):
    global target_day
    if (guess_user.day != target_day):
        return False
    else:
        guess_user_prev = fetchUser(guess_user.mid-1)
        guess_user_prev = validateUser(guess_user_prev,-1)
        if (guess_user_prev.day < guess_user.day):
            return True
        else:
            return False

def resetGuessRange():
    global user_left, user_righ, target_date, target_day, guess_step, guess_mid, guessed_mids
    guessed_mids = []
    guess_step = 1
    user_righ = user_left

def updateTargetDay():
    global target_date, target_day, invalid_mids, guessed_mids, final_day
    target_date = target_date + timedelta(days=1)
    target_day = int(target_date.strftime('%Y%m%d'))

    invalid_mids = []
    guessed_mids = []

    if target_day >= final_day:
        return True
    else:
        return False

def printLog(str):
    logfile = open('log.txt','a')
    # logfile = open('log_test.txt','a')
    print(str)
    print(str,file=logfile)
    logfile.close()

def recordUser(user):
    global target_day, target_date
    userfile = open('user.txt','a')
    # userfile = open('user_test.txt','a')
    if user == 0:
        userstr = '{} {:0>10d} {:0>10s} {} {}'.format(target_day, 0, '0', '0000-00-00 00:00:00', '*')
    else:
        userstr = '{} {:0>10d} {} {} {}'.format(user.day, user.mid, user.timestamp, user.timelocal, user.name)
    printLog('{} {}'.format('++++++++++', userstr))
    print(userstr, file=userfile)
    userfile.close()

def initAll():
    global user_left, user_righ, target_date, target_day, guess_step, guess_mid, invalid_mids, guessed_mids, final_day, fetch_count
    invalid_mids = []
    guessed_mids = []
    final_day = 20180409
    guess_step = 1
    fetch_count = 0
    target_date = date(2018,3,30)
    target_day = int(target_date.strftime('%Y%m%d'))
    user_left = fetchUser(308924710)
    user_righ = user_left
    # target_date = date(2010,9,23)
    # target_day = int(target_date.strftime('%Y%m%d'))
    # user_left = fetchUser(58506)
    # user_righ = fetchUser(58506)

def spider():
    global user_left, user_righ, target_date, target_day, guess_step, guess_mid, invalid_mids
    finished = False
    while not finished:
        printLog('[{} {} ---- {} {}]'.format('left:',user_left.mid,'righ:',user_righ.mid))
        is_today_has_user = guessMid()
        if is_today_has_user == 1:
            guess_user = fetchUser(guess_mid)
            guess_user = validateUser(guess_user)
            is_guess_correct = isGuessCorrect(guess_user)
            if is_guess_correct:
                recordUser(guess_user)
                is_day_full = updateTargetDay()
                if is_day_full:
                    finished = True
                    break
                else:
                    resetGuessRange()
            else:
                updateGuessRange(guess_user)
        elif is_today_has_user == 0: # Target day(s) no user!
            user_righ_datetime = datetime.fromtimestamp(user_righ.timestamp)
            user_righ_date = user_righ_datetime.date()
            gap_days = (user_righ_date - target_date).days
            for i in range(1, gap_days+1):
                recordUser(0)
                updateTargetDay()
            resetGuessRange()
        else:
            break

if __name__ == '__main__':
    initAll()
    spider()
    # fetchUser(103974444)
