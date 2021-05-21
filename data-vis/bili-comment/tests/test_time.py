import datetime
import time

def dt2str(dt_time):
    return "{:>4}-{:0>2}-{:0>2}-{:0>2}-{:0>2}-{:0>2}".format(dt_time.year, dt_time.month, dt_time.day, dt_time.hour, dt_time.minute, dt_time.second)

def str2dt(dt_str):
    return datetime.datetime.strptime(dt_str,'%Y-%m-%d-%H-%M-%S')

def now():
    return datetime.datetime.now()
# now = dt.datetime.now()
# print(now)
# dt_str = dt2str(now)
# print(dt_str)
# dt_time = str2dt(dt_str)
# print(dt_time)
# t1 = str2dt("2020-04-25-18-25-20")
# t2 = str2dt("2020-04-25-19-21-02")
# print((t2-t1).total_seconds())

# t1 = datetime.datetime.now()
# t1 = now()
# time.sleep(0.021)
# # t2 = datetime.datetime.now()
# t2 = now()
# print((t2-t1).total_seconds())

t1 = time.time()
# t1 = now()
time.sleep(0.03002)
t2 = time.time()
# t2 = now()
# print((t2-t1).total_seconds())
print(t2-t1)