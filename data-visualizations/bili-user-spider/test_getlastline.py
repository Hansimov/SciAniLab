from datetime import *

with open('user.txt', 'r') as usrfile:
    for line in usrfile:
        pass
    lastline = line.strip()

print(lastline)
last_mid = int(lastline[9:19].lstrip('0'))
# print(total_num)
last_date_str = lastline[0:8]
last_date_year = int(last_date_str[0:4])
last_date_month = int(last_date_str[4:6])
last_date_day = int(last_date_str[6:8])

target_date = date(last_date_year,last_date_month,last_date_day) + timedelta(days=1)
print(target_date)

# print(datetime.date(2018,4,27) - datetime.timedelta(days=1))
# print(datetime.date.today().strftime('%Y%m%d'))