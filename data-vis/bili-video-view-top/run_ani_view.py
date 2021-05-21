import os
import time

t1 = time.time()

os.system('python ani_view.py')

t2 = time.time()
dt1 = t2 - t1
print('Elapsed time 1: {} s'.format(round(dt1, 2)))
