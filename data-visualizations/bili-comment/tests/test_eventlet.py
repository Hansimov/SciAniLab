import time
t0 = time.time()
import eventlet
eventlet.monkey_patch(thread=False)

t1 = time.time()
try:
    with eventlet.Timeout(0.3):
        time.sleep(0.3)
except eventlet.Timeout as e:
    pass
t2 = time.time()
print(round(t2-t1,1))
print(round(t2-t0,1))
