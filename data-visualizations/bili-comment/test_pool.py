import sys
import random
import time
import multiprocessing

def square(x):
    print(x*x)
    time.sleep(random.random())
    sys.stdout.flush()

if __name__ == "__main__":
    n_L = list(range(1,20))

    pool = multiprocessing.Pool(1)

    pool.imap(square,n_L)
    pool.close()
    pool.join()
