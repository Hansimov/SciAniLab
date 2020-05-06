import time
t0 = time.time()
from gevent import monkey, Timeout
# monkey.patch_all(thread=False)
t1 = time.time()

# try:
with Timeout(0.1):
    time.sleep(0.3)
# except:
#     pass
t2 = time.time()



print(round(t2-t1,1))
print(round(t2-t0,1))
