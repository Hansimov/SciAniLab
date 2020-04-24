import threading
import time
import random
import sys

def job1():
    global cnt, lock
    # global cnt
    # lock.acquire()
    for i in range(10):
        time.sleep(random.random())
        cnt += 1
        print("job1: ",cnt)
        sys.stdout.flush()
    # lock.release()

def job2():
    global cnt, lock
    # global cnt
    # lock.acquire()
    for i in range(10):
        time.sleep(random.random())
        cnt += 1
        print("job2: ",cnt)
        sys.stdout.flush()
    # lock.release()

def is_any_thread_alive(threads):
    return True in [t.is_alive() for t in threads]

if __name__ == "__main__":
    lock = threading.Lock()
    cnt = 0
    t1 = threading.Thread(target=job1,daemon=True)
    t2 = threading.Thread(target=job2,daemon=True)

    t1.start()
    t2.start()

    while is_any_thread_alive([t1,t2]):
        time.sleep(1)
