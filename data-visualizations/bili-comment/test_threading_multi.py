import sys
import time
import random
import threading

n_L = []
def square(x):
    sema.acquire()
    time.sleep(random.random())
    # print(x*x)
    print(x,end=" ")
    lock.acquire()
    sys.stdout.flush()
    n_L.append(x)
    lock.release()
    sema.release()

def is_any_thread_alive(threads):
    return True in [t.is_alive() for t in threads]

if __name__ == '__main__':
    max_concurrent_num = 100
    lock = threading.Lock()
    sema = threading.BoundedSemaphore(max_concurrent_num)

    thread_pool = []
    for i in range(100):
        tmp_thread = threading.Thread(target=square, args=(i+1,), daemon=True)
        thread_pool.append(tmp_thread)

    for tmp_thread in thread_pool:
        tmp_thread.start()

    while is_any_thread_alive(thread_pool):
        time.sleep(0)

    print()
    print(n_L)