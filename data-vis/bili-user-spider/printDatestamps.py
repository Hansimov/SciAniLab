from datetime import *
from time import *

date_head = date(2009, 6, 24)
date_tail = date(2018, 3, 24)

date_delta = date_tail - date_head

# dt = (date_head+timedelta(days=1)).timetuple()
# dt = mktime(dt)
# print(dt)
print(date_delta.days)

datestamps_file = open('datestamps.txt','w')

for i in range(date_delta.days + 1):
    date_tmp = date_head + timedelta(days=i)
    # print(date_tmp)
    date_tmp = date_tmp.timetuple()
    date_tmp = mktime(date_tmp)
    print(date_tmp,file = datestamps_file)
