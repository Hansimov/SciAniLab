import time

t1 = time.time()
time.sleep(1.2)
t2 = time.time()

dt = t2 - t1
print('Elapsed time : {:.5} s'.format(dt))
